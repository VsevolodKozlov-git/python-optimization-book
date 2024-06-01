from ortools.linear_solver import pywraplp


def newSolver(name,integer=False):
    return pywraplp.Solver(name,
                           pywraplp.Solver.
                           CBC_MIXED_INTEGER_PROGRAMMING
                           if integer else
                           pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)


from collections.abc import Iterable


def get_solution_variables(x):
    """

    :param x: Список переменных или переменная
    :return: Значения переменных, если список. Значение переменной, если единственная переменная
    """
    # Если много переменных
    if x is None:
        return 0
    if isinstance(x, Iterable):
        return [get_solution_variables(i) for i in x]
    # Если одна переменная
    if isinstance(x, pywraplp.Variable):
        if x.Integer():
            return int(x.SolutionValue())
        return x.SolutionValue()
    if isinstance(x, int) or isinstance(x, float):
        return x
    raise ValueError('Incorrect type of x')


def get_objective_value(solver):
    """
    :param solver: экземпляр Solver
    :return: Оптимальной значение оптимизируемой функции
    """
    return solver.Objective().Value()
