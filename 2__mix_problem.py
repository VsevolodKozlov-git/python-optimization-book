
from tools import *
from ortools.linear_solver import pywraplp
def solve(crud_oct, crud_cost, ref_oct, ref_cost, money):
    """
    :param сrud_oct: crud_oct[i] =  октановое число для crud типа i
    :param crud_cost:  crud_cost[i] =  стоимость crud типа i
    :param ref_oct: ref_oct[i] =  октановое число для ref типа i
    :param ref_cost: ref_cots[i] = стоимость ref типа i
    :param money: Количество имеющихся денег
    """
    s = pywraplp.Solver('mix',
                        pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    crud_n = len(crud_oct) # Количекство типов crud
    ref_n = len(ref_oct) # Количество типов refined
    # Матрица переменных. x[i][j] - сколько crud газа i использовали для создания refined  газа j
    x = [[s.NumVar(0, 10000, f'{i}{j}') for j in range(ref_n)]
         for i in range(crud_n)]
    # Сколько crud использовали
    crud_used = [s.NumVar(0, s.infinity(), f'crud_used{i}') for i in range(crud_n)]
    for i in range(crud_n):
        s.Add(crud_used[i] == s.Sum(x[i][j] for j in range(ref_n)))
    # Сколько refined получили
    ref_get = [s.NumVar(0, s.infinity(), f'ref_get{j}') for j in range(ref_n)]
    for j in range(ref_n):
        s.Add(ref_get[j] == s.Sum(x[i][j] for i in range(crud_n)))

    # Добавляем условие на пропорцию октанового числа
    for j in range(ref_n):
        weighted_crud_oct = s.Sum(x[i][j]*crud_oct[i] for i in range(crud_n))
        s.Add(weighted_crud_oct == ref_oct[j] * ref_get[j])
    # Добавляем условие на количество потраченных денег
    expenses = s.Sum(crud_used[i]*crud_cost[i] for i in range(crud_n))
    s.Add(expenses <= money)
    revenue = s.Sum(ref_get[j] * ref_cost[j] for j in range(ref_n))

    profit = revenue - expenses
    s.Maximize(profit)
    solution_exit_code = s.Solve()
    return solution_exit_code, get_objective_value(s), get_solution_variables(x)


if __name__ == '__main__':
    solve_result,  obj_val, sol_val = solve(
        [99, 81],
        [55, 53],
        [88, 94],
        [61, 62],
        5000
    )
    print(f'profit: {obj_val}')
    print('x:')
    for row in sol_val:
        print(row)





# from tools import *
# from ortools.linear_solver import pywraplp
# def solve():
#     s = pywraplp.Solver('mix',
#                         pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
#     O = [99, 81] # октановое число crud
#     c = [55, 54] # стоимость crud
#     o = [88, 94] # октановое число refined
#     v = [61, 62] # стоимость refined
#     m = 5000 # количество денег
#     rr = len(O) # Количекство crud
#     fr = len(o) # Количество refined
#     # Матрица решений. по G[i][j] - сколько crud газа i использовали
#     # для создания refined  газа j
#     G = [[s.NumVar(0, 10000, f'{i}{j}') for j in range(fr)]
#          for i in range(rr)]
#     # Сколько crud использовали
#     R = [s.Sum(G[i][j] for j in range(fr)) for i in range(rr)]
#     # Сколько refined получили
#     F = [s.Sum(G[i][j] for i in range(rr)) for j in range(fr)]
#     # Максимизировать проданный crud
#     max_func = s.Sum(F[j]*v[j] for j in range(fr))
#     # Добавляем условие на концентрацию для получения газа
#     for j in range(fr):
#         weighted_crud_oct = s.Sum(G[i][j]*O[i] for i in range(rr))
#         s.Add(weighted_crud_oct == F[j]*o[j])
#     # Добавляем условие на количество потраченных денег
#     s.Add(s.Sum(R[i]*c[i] for i in range(rr)) <= m)
#     s.Maximize(max_func)
#     solution_exit_code = s.Solve()
#     return solution_exit_code, ObjVal(s), SolVal(G)
#
#
# if __name__ == '__main__':
#     solve_result,  obj_val, sol_val = solve()
#     print(solve_result, obj_val, sol_val)