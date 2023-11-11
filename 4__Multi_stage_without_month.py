from ortools.linear_solver import pywraplp

def solve():
    s = pywraplp.Solver('oil_soap_planning',
                        pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
    oi_ac = [[36, 20, 33],
         [0, 68, 13],
         [0, 6, 0],
         [0, 32, 0],
         [0, 0, 49],
         [45, 0, 40],
         [0, 0, 0],
         [36, 55, 0],
         [12, 48, 34]]
    so_ac_range = [[13.3, 23.2, 17.8],
         [14.6, 25.7, 19.7]]
    pr_mo = [[118, 128],
         [161, 152],
         [129, 191],
         [103, 110],
         [127, 100],
         [171, 166],
         [171, 131],
         [147, 123]]
    held_initial = [15, 52, 193, 152, 70, 141, 42, 25, 89]

    demand = 5000
    storage = 1000
    stor_price = 5
    n_ac = len(oi_ac[0])
    n_oi = len(oi_ac)
    n_so = len(so_ac_range)
    n_mo = len(pr_mo[0])
    oi_bo = [[s.NumVar(0, 5000, '') for j in range(n_mo)]
             for i in range(n_oi)]
    oi_us = [[s.NumVar(0, 5000, '') for j in range(n_mo)]
             for i in range(n_oi)]

    # Добавим oi_held
    # oi_held[oi][mo] - сколько остатолось масла oi на начало месяца mo
    oi_held = [[None for j in range(n_mo)] for i in range(n_oi)]
    for j_mo in range(n_mo):
        for i_oi in range(n_oi):
            if j_mo == 0:
                oi_held[i_oi][j_mo] = held_initial[i_oi]
        else:
            used = oi_us[i_oi][j_mo]
            bought = oi_bo[i_oi][j_mo]
            prev_held = oi_held[i_oi][j_mo-1]
            oi_held[i_oi][j_mo] = bought + prev_held - used

    # Условие на кислотное содержание масла
    mo_j = 0
    for j_ac in range(n_ac):
        sm_oi = 0
        wg_oi_ac = 0
        for i_oi in range(n_oi):
            ac_perc = oi_ac[i_oi][j_ac]
            oi_used = oi_us[i_oi][mo_j]
            sm_oi += oi_used
            wg_oi_ac += oi_used * ac_perc
        lower = so_ac_range[0][j_ac]
        s.Add(wg_oi_ac >= lower*sm_oi)

        upper = so_ac_range[1][j_ac]
        s.Add(wg_oi_ac <= upper*sm_oi)

    # used не должно превышать bought+oi_held
    for j_mo in range(n_mo):
        for i_oi in range(n_oi):
            bought = oi_bo[i_oi][j_mo]
            held = oi_held[i_oi][j_mo]
            used = oi_us[i_oi][j_mo]
            s.Add(used <= bought+held)
    # oi_us в каждом месяце == 5000
    sum_month_used = [s.NumVar(0, 5000, '') for mo in range(n_mo)]
    for j_mo in range(n_mo):
        s.Add(sum_month_used[j_mo] == s.Sum([oi_us[i][j_mo] for i in range(n_oi)]))
    # oi_held не должно превышать 1000 в каждом месяце
    sum_month_held = [s.NumVar(0, 1000, '') for mo in range(n_mo)]
    for j_mo in range(n_mo):
        s.Add(sum_month_held[j_mo] == s.Sum([oi_held[i][j_mo] for i in range(n_oi)]))

    costs = 0
    # за oi_held в каждом месяце платим 5$/тонна
    costs += s.Sum(sum_month_held) * 5
    # за покупку платим по прайслисту
    for i_oi in range(n_oi):
        for j_mo in range(n_mo):
            price = pr_mo[i_oi][j_mo]
            bought = oi_bo[i_oi][j_mo]
            costs += price * bought
    s.Minimize(costs)
    s.Solve()