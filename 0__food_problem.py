from ortools.linear_solver import pywraplp
from tools import get_objective_value, get_solution_variables


def solve(food_creature, food_amount):
    """
    :param food_creature:
    Таблица n x m где в ячейке food_creature[i][j] хранится сколько пищи i потребляет животное j
    :param food_amount:
    Список длинной m, где значение food_amount[i] означает сколько пищи i есть в наличии
    :return:
    Общее количество животных. Количество животных каждого типа
    """
    pass
    # Создаем экземпляр решателя
    s = pywraplp.Solver('food_solver', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
    # Записываем количество животных и еды в переменные
    food_n = len(food_creature)
    creat_n = len(food_creature[0])
    # Инициализируем переменные
    creat_x = [s.NumVar(0, s.infinity(), '') for i in range(creat_n)]
    food_eaten = [s.NumVar(0, food_amount[i], '') for i in range(food_n)]
    creat_sum = s.Sum(creat_x)
    # Присваиваем значение переменным и задаем ограничения
    for food_i in range(food_n):
        # Количество съеденной пищи == сумме пищи, съеденной каждым животны
        s.Add(food_eaten[food_i] ==
              s.Sum(creat_x[creat_j] * food_creature[food_i][creat_j] for creat_j in range(creat_n)))
        # Вообще это условие необязательно, ведь мы задали верхнее ограничение при инициализации в строке:
        # food_eaten = [s.NumVar(0, food_amount[i], '') for i in range(food_n)]
        s.Add(food_eaten[food_i] <= food_amount[food_i])
    # Решаем задачу
    s.Maximize(creat_sum)
    solver_code = s.Solve() # если solver_code == 0, то оптимизация прошла успешно
    # Возвращаем результат
    return solver_code, get_objective_value(s), get_solution_variables(creat_x)


def solve_integer(food_creature, food_amount):
    """
    :param food_creature:
    Таблица n x m где в ячейке food_creature[i][j] хранится сколько пищи i потребляет животное j
    :param food_amount:
    Список длинной m, где значение food_amount[i] означает сколько пищи i есть в наличии
    :return:
    Общее количество животных. Количество животных каждого типа
    """
    pass
    # Создаем экземпляр решателя
    s = pywraplp.Solver('food_solver', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    # Записываем количество животных и еды в переменные
    food_n = len(food_creature)
    creat_n = len(food_creature[0])
    # Инициализируем переменные
    creat_x = [s.IntVar(0, s.infinity(), '') for i in range(creat_n)]
    food_eaten = [s.IntVar(0, food_amount[i], '') for i in range(food_n)]
    creat_sum = s.Sum(creat_x)
    # Присваиваем значение переменным и задаем ограничения
    for food_i in range(food_n):
        # Количество съеденной пищи == сумме пищи, съеденной каждым животны
        s.Add(food_eaten[food_i] ==
              s.Sum(creat_x[creat_j] * food_creature[food_i][creat_j] for creat_j in range(creat_n)))
        # Вообще это условие необязательно, ведь мы задали верхнее ограничение при инициализации в строке:
        # food_eaten = [s.NumVar(0, food_amount[i], '') for i in range(food_n)]
        s.Add(food_eaten[food_i] <= food_amount[food_i])
    # Решаем задачу
    s.Maximize(creat_sum)
    solver_code = s.Solve() # если solver_code == 0, то оптимизация прошла успешно
    # Возвращаем результат
    return solver_code, get_objective_value(s), get_solution_variables(creat_x)


if __name__ == '__main__':
    food_creature = [[2, 2, 0],
                     [0, 1, 3]]
    food_amount = [3000, 5000]
    # print(solve(food_creature, food_amount))

    a1 = [[3, 2, 0],
          [0, 2, 0],
          [0, 2, 3]]
    a2 = [5, 2, 5]
    print(solve(a1, a2))