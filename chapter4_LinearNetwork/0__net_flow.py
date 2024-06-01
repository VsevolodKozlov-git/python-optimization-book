from tools import *
from ortools.linear_solver import pywraplp


def optimize_net(graph, sources, sinks):
    """
    :param graph:
    graph[i][j] == количеству единиц транспортируемых из вершины i в ji to j
    :param sources:
    Список индексов источников
    :param sinks:
    Список индексов стоков
    """
    # Создаем экземпляр solver
    s = pywraplp.Solver(
        'net flow solver',
        pywraplp.Solver.GLOP_LINEAR_PROGRAMMING
    )
    # Создаем переменные и добавляем ограничения на них
    n = len(graph)

    def var_or_0(i, j):
        if graph[i][j] == 0:
            return 0
        return s.NumVar(0, graph[i][j], '')
    x = [[var_or_0(i, j) for j in range(n)]
         for i in range(n)]

    flow_in = [s.Sum(x[i][j] for i in range(n))
               for j in range(n)]
    flow_out = [s.Sum(x[i][j] for j in range(n))
                for i in range(n)]
    for i in range(n):
        if (i not in sources) and (i not in sinks):
            s.Add(flow_in[i] == flow_out[i])

    # Инициализируем фиктивные переменные
    all_nodes_sum = sum(graph[i][j] for i in range(n) for j in range(n))
    source_out = s.NumVar(0, all_nodes_sum, '') # сколько пришло в источник
    s.Add(source_out == s.Sum(flow_out[i] for i in sources))
    source_in = s.NumVar(0, all_nodes_sum, '') # сколько ушло из истоничка
    s.Add(source_in == s.Sum(flow_in[i] for i in sources))
    # Функция максимизации
    max_func = source_out - 2 * source_in
    s.Maximize(max_func)
    solution_exit_code = s.Solve()
    # return solution
    return solution_exit_code, get_objective_value(s), get_solution_variables(x)


if __name__ == '__main__':
    n = 6
    graph = [[0 for j in range(n)]
             for i in range(n)]
    i_j_vals = [
        [0, 1, 20],
        [0, 2, 20],
        [1, 2, 10],
        [1, 3, 20],
        [2, 4, 10],
        [3, 4, 15],
        [3, 5, 10],
        [4, 5, 20]
    ]
    for i, j, val in i_j_vals:
        graph[i][j] =val
    sources = [0]
    sinks = [5]
    solve_result, obj_val, sol_val = optimize_net(graph, sources, sinks)
    print(f'max flow:{obj_val}')
    for row in sol_val:
        print(row)


