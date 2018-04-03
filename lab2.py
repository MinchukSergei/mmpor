from ortools.graph import pywrapgraph


def main():
    with open('lab2data.txt') as file:
        worker_groups = list(map(int, file.readline().split(' ')))
        task_groups = list(map(int, file.readline().split(' ')))
        cost = []
        for i in range(len(worker_groups)):
            cost.append(list(map(int, file.readline().split(' '))))

    worker_num = sum(worker_groups)
    task_num = sum(task_groups)

    efficiency = [[0 for x in range(task_num)] for y in range(worker_num)]
    workers_and_tasks = [[(0, 0) for x in range(task_num)] for y in range(worker_num)]

    row_ind = 0
    col_ind = 0

    for i, worker_group in enumerate(worker_groups):
        for j, task_group in enumerate(task_groups):
            for k in range(worker_group):
                for l in range(task_group):
                    efficiency[k + row_ind][l + col_ind] = -cost[i][j]
                    workers_and_tasks[k + row_ind][l + col_ind] = (i + 1, j + 1)
            col_ind += task_group
        row_ind += worker_group
        col_ind = 0

    assignment = pywrapgraph.LinearSumAssignment()

    for worker in range(worker_num):
        for task in range(task_num):
            if efficiency[worker][task]:
                assignment.AddArcWithCost(worker, task, efficiency[worker][task])

    solve_status = assignment.Solve()
    if solve_status == assignment.OPTIMAL:
        print(f'Total efficiency: {-assignment.OptimalCost()}')
        print()
        for i in range(assignment.NumNodes()):
            worker = i
            group = assignment.RightMate(i)
            efficiency = -assignment.AssignmentCost(i)
            w, t = workers_and_tasks[worker][group]
            print(f'Worker from group {w} assigned to task type {t}, efficiency: {efficiency}')

    elif solve_status == assignment.INFEASIBLE:
        print('No assignment is possible.')
    elif solve_status == assignment.POSSIBLE_OVERFLOW:
        print('Some input costs are too large and may cause an integer overflow.')


if __name__ == '__main__':
    main()
