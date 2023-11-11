
from tools import *
from ortools.linear_solver import pywraplp
def solve():
    s = pywraplp.Solver('mix',
                        pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
    O = [99, 81] # октановое число crud
    c = [55, 54] # стоимость crud
    o = [88, 94] # октановое число refined
    v = [61, 62] # стоимость refined
    m = 5000 # количество денег
    rr = len(O) # Количекство crud
    fr = len(o) # Количество refined
    # Матрица решений. по G[i][j] - сколько crud газа i использовали
    # для создания refined  газа j
    G = [[s.NumVar(0, 10000, f'{i}{j}') for j in range(fr)]
         for i in range(rr)]
    # Сколько crud использовали
    R = [s.NumVar(0, 10000, f'R{i}') for i in range(rr)]
    for i in range(rr):
        s.Add(R[i] == s.Sum(G[i][j] for j in range(fr)))
    # Сколько refined получили
    F = [s.NumVar(0, 10000, f'R{j}') for j in range(fr)]
    for j in range(fr):
        s.Add(F[j] == s.Sum(G[i][j] for i in range(rr)))
    # Максимизировать проданный crud
    max_func = s.Sum(F[j]*v[j] for j in range(fr))
    # Добавляем условие на концентрацию для получения газа
    for j in range(fr):
        # Деление нельзя использовать, потому что это не линейная операция
        # Код ниже не будет работать:
        """
        res_oct = s.Sum(G[i][j]*O[i] for i in range(rr)) / F[j]
        s.Add(res_oct == o[j])
        """
        weighted_crud_oct = s.Sum(G[i][j]*O[i] for i in range(rr))
        s.Add(weighted_crud_oct == o[j] * F[j])
    # Добавляем условие на количество потраченных денег
    s.Add(s.Sum(R[i]*c[i] for i in range(rr)) <= m)
    s.Maximize(max_func)
    solution_exit_code = s.Solve()
    return solution_exit_code, ObjVal(s), SolVal(G)


if __name__ == '__main__':
    solve_result,  obj_val, sol_val = solve()
    print(solve_result, obj_val, sol_val)





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