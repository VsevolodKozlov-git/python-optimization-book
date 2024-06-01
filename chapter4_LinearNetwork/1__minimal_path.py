from tools import *
from ortools.linear_solver import pywraplp




def solve(graph, start, end):
    """
    :param graph:
    graph[i][j] == None, если пути нет.
    grapht[i][j] = число, если путь есть и его стоимость равняется числу
    """
    # Создаем экземпляр solver
    s = pywraplp.Solver(
        'net flow solver',
        pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING
    )
    n = len(graph)

    def get_0_or_var(i, j):
        if graph[i][j] is None:
            return 0
        return s.IntVar(0, 1, '')

    x = [[get_0_or_var(i, j) for j in range(n)]
         for i in range(n)]
    for node in range(n):
        # Сколько раз входим в node
        in_paths_var = s.IntVar(0, 1, '')
        s.Add(in_paths_var == s.Sum(x[i][node] for i in range(n)))
        # Сколько раз выходим из node
        out_paths_var = s.IntVar(0, 1, '')
        s.Add(out_paths_var == s.Sum(x[node]))
        if node == start:
            s.Add(in_paths_var == 0)
            s.Add(out_paths_var == 1)
        elif node == end:
            s.Add(in_paths_var == 1)
            s.Add(out_paths_var == 0)
        else:
            s.Add(in_paths_var == out_paths_var)


    def get_path(i, j):
        if graph[i][j] is None:
            return 0
        return x[i][j] * graph[i][j]
    path_sum = s.Sum([get_path(i, j) for i in range(n) for j in range(n)])
    s.Minimize(path_sum)
    solver_code = s.Solve()
    solution_matrix = get_solution_variables(x)
    path = get_path_from_solution_matrix(solution_matrix, start, end)
    return solver_code, get_objective_value(s),  path


def get_path_from_solution_matrix(matrix, start, end):
    n = len(matrix)
    path = [start]
    ind = start
    while ind != end:
        for i in range(n):
            if matrix[ind][i] == 1:
                ind = i
                path.append(i)
                break
    return path

if __name__ == '__main__':
    graph = [[None, 2, 3, None, None],
             [None, None, None, 5, 7],
             [None, 5, None, None, None],
             [None, None, 5, None, 1],
             [None, None, None, None, None]] # длина - 8
    start = 0
    end = 4
    code, path_len, path = solve(graph, start, end)
    print(path_len)
    print(path)

