from ortools.linear_solver import pywraplp

def example():
    s = pywraplp.Solver('name',pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
    x1 = s.NumVar(0, 1000, '')
    x2 = s.NumVar(0, 1000, '')
    res = s.NumVar(0, 1000, '')
    s.Add(5*x1-2*x2 <= 7)
    s.Add(-1*x1+2*x2 <= 5)
    s.Add(x1+x2 >= 6)
    s.Add(res == x1+2*x2)
    s.Maximize(res)
    solution = s.Solve()
    return x1.SolutionValue()


if __name__ == '__main__':
    print(example())
    # solution, res, x1, x2 = example()
    # print(res.SolutionValue())
