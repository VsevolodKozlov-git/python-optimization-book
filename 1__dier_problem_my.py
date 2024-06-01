from ortools.linear_solver import pywraplp
import numpy as np
from tools import get_objective_value, get_solution_variables


def solve(ing_nutr, ing_cost, ing_max, nutr_min):
    """
    :param ing_nutr: ing_nutr[i][j] - сколько вещества j в игредиенте i
    :param ing_cost: ing_cost[i] - сколько стоит ингредиент i
    :param ing_max: ing_max[i] - максимальное количество игредиента i
    :param nutr_min: nutr_min[i] - какое минимальное количество вещества i необходимо
    """
    s = pywraplp.Solver('food solver',
                        pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
    ing_n = len(ing_nutr) # Количество игредиентов
    nutr_n = len(ing_nutr[0]) # Количество веществ
    # Объявим переменную
    x = [s.NumVar(0, ing_max[i], f'x[{i}]') for i in range(ing_n)]
    # Количество полезных веществ должно быть больше минимума
    for j in range(nutr_n):
        s.Add(s.Sum(x[i] * ing_nutr[i][j] for i in range(ing_n)) >= nutr_min[j])
    # Введем переменную для затрат
    costs = s.NumVar(0, s.infinity(), 'costs')
    s.Add(costs == s.Sum([x[i] * ing_cost[i] for i in range(ing_n)]))
    # Минимизируем затраты
    s.Minimize(costs)
    solution_code = s.Solve()
    return solution_code, get_objective_value(s), get_solution_variables(x)


if __name__ == '__main__':
    ing_nutr = [[785, 4928, 843, 26],
    [946, 7973, 7302, 77],
    [570, 5172, 6106,49]]
    ing_cost = [4.14, 6.6,	6.6]
    ing_max = [20, 20, 15]
    nutr_min = [41120, 13598, 14260, 601]
    status_code, costs, x = solve(ing_nutr, ing_cost, ing_max, nutr_min)
    print(f'status code: {status_code}')
    print(f'Затраты: {costs}')
    print(f'Количество игредиентов:{x}')