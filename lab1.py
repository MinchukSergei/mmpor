from ortools.linear_solver import pywraplp

coefficients = [
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 0],  # full time 1
    [0, 0, 1, 1, 1, 0, 1, 1, 1, 1],  # full time 2
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],  # part time 1
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 0],  # part time 2
    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0],  # part time 3
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],  # part time 4
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0],  # part time 5
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],  # part time 6
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1]  # part time 7
]

constraints = [
    16, 30, 31, 45, 66, 72, 61, 34, 16, 10
]

objective_coefficients = [
    8 * 8, 8 * 8, 4 * 6, 4 * 7, 4 * 9, 4 * 10, 4 * 8, 4 * 6, 4 * 6
]

worker_types = [
    'full1', 'full2', 'part1', 'part2', 'part3', 'part4', 'part5', 'part6', 'part7'
]


class Schedule:
    def __init__(self):
        self.solver = pywraplp.Solver('SolveIntegerProblem',
                                      pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
        self.variables = []
        self.solver_constraints = []
        self.result = False
        self.objective = self.solver.Objective()
        self.build_schedule()

    def build_schedule(self):
        solver = self.solver
        variables = self.variables
        solver_constraints = self.solver_constraints
        objective = self.objective

        for wt in worker_types:
            variables.append(solver.IntVar(0.0, solver.Infinity(), wt))

        for i, c in enumerate(constraints):
            solver_constraint = solver.Constraint(c, solver.Infinity())
            for j, variable in enumerate(variables):
                solver_constraint.SetCoefficient(variable, coefficients[j][i])
            solver_constraints.append(solver_constraint)

        for i, c in enumerate(objective_coefficients):
            objective.SetCoefficient(variables[i], c)

        objective.SetMinimization()

    def solve(self):
        self.result = self.solver.Solve()

    def print_solution(self):
        optimal = self.result == pywraplp.Solver.OPTIMAL
        verified = optimal and self.solver.VerifySolution(1e-4, True)

        print(f'Optimal: {optimal}')
        print(f'Verified: {verified}')

        if not optimal or not verified:
            return

        for v in self.variables:
            print(f'{v.name()}: {v.solution_value()}')

        print(f'Optimal objective value: {self.objective.Value()}')


def main():
    print('part a:')
    schedule_a = Schedule()
    schedule_a.solve()
    schedule_a.print_solution()
    print()

    print('part b:')
    schedule_b = Schedule()

    full_time_solver_constraint = schedule_b.solver.Constraint(4, schedule_b.solver.Infinity())
    full_time_solver_constraint.SetCoefficient(schedule_b.variables[0], 1)
    full_time_solver_constraint.SetCoefficient(schedule_b.variables[1], 1)
    schedule_b.solver_constraints.append(full_time_solver_constraint)

    schedule_b.solve()
    schedule_b.print_solution()
    print()

    print('part c:')
    schedule_c = Schedule()

    stuff_number_constraint = schedule_c.solver.Constraint(0, 94)
    for v in schedule_c.variables:
        stuff_number_constraint.SetCoefficient(v, 1)
    schedule_c.solver_constraints.append(stuff_number_constraint)

    schedule_c.solve()
    schedule_c.print_solution()


if __name__ == '__main__':
    main()
