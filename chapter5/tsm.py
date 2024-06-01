from ortools.linear_solver import pywraplp
from tools import *


def solve_tsp(graph):
    all_subtours = []
    tours = []
    iter = 0
    while len(tours) != 1:
        code, distance, tours = solve_with_subtours(graph, all_subtours)
        all_subtours.extend(tours)
        print(f'iteration: {iter}')
        print(distance)
        print(tours)
        print('-'*20)
        iter += 1



def solve_with_subtours(graph, subtours):
    # BC_MIXED_INTEGER_PROGRAMMING не работает
    s = pywraplp.Solver(
        'tsm',
        pywraplp.Solver.SAT_INTEGER_PROGRAMMING
    )
    n = len(graph)
    x = [[s.NumVar(0, 1, '') for j in range(n)]
         for i in range(n)]

    for ind in range(n):
        # add col constraint
        s.Add(s.Sum(x[i][ind] for i in range(n)) == 1)
        # add row constraint
        s.Add(s.Sum(x[ind][j] for j in range(n)) == 1)
        s.Add(x[ind][ind] == 0)

    for sub in subtours:
        K = []
        for i in range(len(sub)):
            index_i = sub[i]
            for j in range(len(sub)):
                index_j = sub[j]
                if i != j:
                    arc = x[index_i][index_j]
                    K.append(arc)
        s.Add(len(sub)-1 >= sum(K))
    min_func = s.NumVar(0, 100000, '')
    s.Add(min_func == s.Sum(x[i][j] * (graph[i][j] if graph[i][j] is not None else 0)
                            for j in range(n) for i in range(n) ))
    s.Minimize(min_func)
    solve_code = s.Solve()
    tours = extract_tours(get_solution_variables(x))
    return solve_code, get_objective_value(s), tours


def extract_tours(x):
    n = len(x)
    node = 0
    tours = [[0]]
    all_nodes = [0] + [1]*(n-1)
    while sum(all_nodes) > 0:
        next = [i for i in range(n) if x[node][i] == 1][0]
        if next not in tours[-1]:
            tours[-1].append(next)
            node = next
        else:
            node = all_nodes.index(1)
            tours.append([node])
        all_nodes[node] = 0
    return tours


    # strs = [
    #     "711 107 516 387 408 539 309 566 771",
    #     "539 769 881 380 546 655 443 295 1140",
    #     '122 752 281 441 264 318 448 588 730',
    #     '519 875 274 435 334 93 776 949 302',
    #     '484 561 338 419 118 268 607 495 431',
    #     '409 406 244 380 93 295 544 549 494',
    #     '479 735 334 101 345 247 679 809 238',
    #     '221 444 433 744 487 435 649 325 840',
    #     '510 303 599 984 531 553 847 350 1001',
    #     '663 989 664 335 588 434 297 1093 1012'
    # ]
    # graph = []
    # for i in range(len(strs)):
    #     row = list(map(int, strs[i].split()))
    #     row.insert(i, None)
    #     graph.append(row)

if __name__ == '__main__':
    graph = [[None, 7, 6, 5, 8],
             [8, None, 5, 6, 9],
             [8, 6, None, 7, 4],
             [7, 8, 7, None, 8],
             [6, 9, 8, 5, None]]
    solve_tsp(graph)