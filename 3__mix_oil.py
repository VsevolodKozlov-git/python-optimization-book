"""
Задача со страницы 49
"""
from tools import *
from ortools.linear_solver import pywraplp


def solve():
    s = pywraplp.Solver('oil_solver', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
    c = [110, 120, 130, 110, 115]
    h = [8.8, 6.1, 2, 4.2, 5]
    no = len(c)
    o = [s.NumVar(0, 200, str(i)) for i in range(no)]

    o_sum = s.NumVar(0, 10000, 'oil_weight_sum')
    s.Add(o_sum == s.Sum(o))

    o_w_sum = s.NumVar(0, 100000, 'oil weighted sum')
    s.Add(o_w_sum == s.Sum(o[i]*h[i] for i in range(no)))

    # costs
    costs = s.NumVar(0, 100000, 'costs')
    s.Add(costs == s.Sum(o[i]*c[i] for i in range(no)))

    # profit
    profit = s.NumVar(0, 100000, 'profit')
    s.Add(profit == o_sum*150-costs)
    # Условие на плотность масла
    s.Add(o_w_sum >= 3*o_sum)
    s.Add(o_w_sum <= 6*o_sum)

    # Условие на ограничения по производству малса
    s.Add(o[0]+o[1] <= 200)
    s.Add(o[2]+o[3]+o[4] <= 250)

    s.Maximize(profit)
    solver_exit_code = s.Solve()
    return solver_exit_code, ObjVal(s), SolVal(o)


if __name__ == '__main__':
    print(solve())