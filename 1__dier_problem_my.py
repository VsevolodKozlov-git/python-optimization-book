from ortools.linear_solver import pywraplp
import numpy as np

N = np.array([[1, 2, 1],
              [2, 1, 1]])
cost = [3, 4]
f_mn = [0, 0]
f_mx = [20, 20]
n_mn =[10, 20, 10]

def solve():
    s = pywraplp.Solver('food solver',
                        pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
    nf = len(N)
    nn = len(N[0])
    f = [s.NumVar(f_mn[i], f_mx[i], f'f[{i}]') for i in range(nf)]
    res = s.NumVar(0, 1000, 'result')
    for j in range(nn):
        s.Add(s.Sum(f[i]*N[i, j] for i in range(nf)) >= n_mn[j])
    s.Add(res == s.Sum([f[i]*cost[i] for i in range(nf)]))
    s.Minimize(res)
    s.Solve()
    # SolutionValue может быть получен только внутри одной области видимости. Такова жизнь(
    return f[0].SolutionValue()


if __name__ == '__main__':
    print(solve())
    # print([e.SolutionValue() for e in f])
