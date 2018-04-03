from math import sqrt


def calc_q0(daily_consume, cost_of_batch, daily_storing_cost):
    return sqrt(2 * daily_consume * cost_of_batch / daily_storing_cost)


def calc_qn(daily_consume, delivery_duration, n):
    return daily_consume * delivery_duration / n


def optimize(q0, daily_consume, product_number):
    q_next = 0
    q_prev = 0
    n = 1

    while not (q_next < q0 <= q_prev):
        q_prev = q_next
        q_next = calc_qn(daily_consume, product_number, n)
        n += 1

    return q_prev, q_next, n


def calc_average_costs(daily_consume, cost_of_batch, daily_storing_cost, q):
    return (daily_consume * cost_of_batch / q) + (daily_storing_cost * q / 2)


def main():
    product_number = 24000
    delivery_duration = 365
    cost_storing_per_month = 0.1
    cost_of_batch = 350

    daily_consume = product_number / delivery_duration
    daily_storing_cost = cost_storing_per_month * 12 / delivery_duration
    q0 = calc_q0(daily_consume, cost_of_batch, daily_storing_cost)

    q1, q2, n = optimize(q0, daily_consume, product_number)

    f1 = calc_average_costs(daily_consume, cost_of_batch, cost_storing_per_month, q1)
    f2 = calc_average_costs(daily_consume, cost_of_batch, cost_storing_per_month, q2)

    optimal_batch_size = q1 if f1 < f2 else q2
    optimal_interval = delivery_duration / (product_number / optimal_batch_size)

    print(f'Optimal batch size: {optimal_batch_size}')
    print(f'Optimal interval: {optimal_interval}')


if __name__ == '__main__':
    main()
