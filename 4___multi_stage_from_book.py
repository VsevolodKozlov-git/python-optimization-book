import random

from tools import *
from random import randint, uniform, seed
seed(10)

def gen_data_content(m,n):
    # Oils down, acids accross (more oils than acids  m > n)
    R=[]
    for i in range(m):
        RR=[]
        P = 100
        for j in range(n-1):
            if P>1:
                acid = randint(1,min(70,P))*randint(0,1)
            else:
                acid = 0
            RR.append(acid)
            P -= acid
        RR.append(P)
        R.append(RR)
    return R
def gen_data_target(C):
    F = []
    R0,R1 = [],[]
    m,n = len(C),len(C[0])
    P = 100
    R = [0 for j in range(n)]
    for i in range(m-1):
        if P:
            f=randint(1,min(20,P))
        else:
            f=0
        F.append(f)
        P-=f
        for j in range(n):
            acid = f*C[i][j]
            R[j] += acid
    f=P
    F.append(f)
    for j in range(n):
        acid = f*C[m-1][j]
        R[j] += acid
    for j in range(n):
        R0.append((0.95*R[j]/100.0))
        R1.append((1.05*R[j]/100.0))
    return [R0,R1]


def gen_data_cost(m,k):
    # Oils down, months accross
    R=[]
    for i in range(m):
        RR=[]
        for j in range(k):
            cost = randint(100,200)
            RR.append(cost)
        R.append(RR)
    return R
def gen_data_inventory(m):
    # Oils down
    R=[]
    for i in range(m):
        cost = [randint(0,200)]
        R.append(cost)
    return R


def solve_model(oil_acid, acid_bound, oil_cost, oil_held, demand, stor_cost, stor_bound):
    s = newSolver('Multi-period soap blending problem')
    Oils= range(len(oil_acid))
    Periods = len(oil_cost[0])
    Acids = len(oil_acid[0])
    Buy = [[s.NumVar(0, demand, '') for _ in range(Periods)] for _ in Oils]
    Blnd = [[s.NumVar(0, demand, '') for _ in range(Periods)] for _ in Oils]
    Hold = [[s.NumVar(0, demand, '') for _ in range(Periods)] for _ in Oils]
    # Сколько произвели в месяц
    month_prod = [s.NumVar(0, demand, '') for _ in range(Periods)]
    month_oil_costs= [s.NumVar(0, demand * 1000, '') for _ in range(Periods)]
    month_storage_costs= [s.NumVar(0, demand * 1000, '') for _ in range(Periods)]
    mon_weigh_acid = [[s.NumVar(0, demand * demand, '') for _ in range(Periods)] for _ in range(Acids)]
    # Дано oil изначально
    for i in Oils:
        s.Add(Hold[i][0] == oil_held[i][0])
    for j in range(Periods):
        # Сколько произвели в месяц
        s.Add(month_prod[j] == sum(Blnd[i][j] for i in Oils))
        # Произоводство должно удовлетворять demand. Причем мы пишем ">="
        # потому что все равно минимизируем
        s.Add(month_prod[j] >= demand)

        # Рассчитываем hold для следующего месяца
        if j < Periods-1:
            for i in Oils:
                s.Add(Hold[i][j]+Buy[i][j]-Blnd[i][j] == Hold[i][j+1])
        # Hold не должно превышать количество
        s.Add(sum(Hold[i][j] for i in Oils) >= stor_bound[0])
        s.Add(sum(Hold[i][j] for i in Oils) <= stor_bound[1])

        # Рассчитываем концентрацию кислоты и накладываем условия
        for k in range(Acids):
            s.Add(mon_weigh_acid[k][j] == sum(Blnd[i][j] * oil_acid[i][k] for i in Oils))
            s.Add(mon_weigh_acid[k][j] >= acid_bound[0][k] * month_prod[j])
            s.Add(mon_weigh_acid[k][j] <= acid_bound[1][k] * month_prod[j])

        # Рассчитываем затраты
        s.Add(month_oil_costs[j] == sum(Buy[i][j] * oil_cost[i][j] for i in Oils))
        s.Add(month_storage_costs[j] == sum(Hold[i][j] * stor_cost for i in Oils))
    Cost_product = s.Sum(month_oil_costs[j] for j in range(Periods))
    Cost_storage = s.Sum(month_storage_costs[j] for j in range(Periods))
    s.Minimize(Cost_product+Cost_storage)
    rc = s.Solve()
    B,L,H,A = get_solution_variables(Buy), get_solution_variables(Blnd), get_solution_variables(Hold), get_solution_variables(mon_weigh_acid)
    CP,CS,P = get_solution_variables(month_oil_costs), get_solution_variables(month_storage_costs), get_solution_variables(month_prod)
    return rc, get_objective_value(s), B, L, H, P, A, CP, CS

def test_data_target():
    print(gen_data_target([[1, 2, 3],
                    [3, 4, 5]]))


if __name__ == '__main__':
    oils = 5
    acids = 3
    month = 2
    part = gen_data_content(oils, acids)

    target = gen_data_target(part)
    cost = gen_data_cost(oils, month)
    inventory = gen_data_inventory(oils)
    demand = 5000
    storage_cost = 5
    storage_bound = [0, 1000]


    print(solve_model(part, target, cost, inventory, demand, storage_cost, storage_bound))

