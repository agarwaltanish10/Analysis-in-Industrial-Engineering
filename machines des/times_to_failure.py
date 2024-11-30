import numpy as np
import matplotlib.pyplot as plt
np.random.seed(1234)

def failure():
    global s, area, possible_times, next_failure, next_repair, t_last, s_last, clock, repairs
    s = s - 1
    if s > 0:
        next_failure = clock + np.random.choice(possible_times)
        new_repair_time = np.random.choice([4.5, 6.5], p=[0.4, 0.6])
        repairs = np.append(repairs, clock + new_repair_time)
        min_time = np.min(repairs)
        next_repair = min_time

    area = area + s_last * (clock - t_last)
    t_last = clock
    s_last = s
    
def repair():
    global s, area, possible_times, next_failure, next_repair, t_last, s_last, clock, repairs  
    s = s + 1
    if s < n:
        new_repair_time = np.random.choice([4.5, 6.5], p=[0.4, 0.6])
        repairs = np.append(repairs, clock + new_repair_time)
        arg_min_time = np.argmin(repairs)
        repairs[arg_min_time] = INFTY
        min_time = np.min(repairs)
        next_repair = min_time
    
    elif s == n:
        next_repair = INFTY
        repairs = np.array([INFTY])
    
    area = area + s_last * (clock - t_last)
    t_last = clock
    s_last = s

    
def timer():
    global clock, next_failure, next_repair, times
    event = 'f'
    if next_failure < next_repair:
        event = 'f'
        clock = next_failure
    else:
        event = 'r'
        clock = next_repair
    return event 

avg_failure_times = np.zeros(4)
avg_machines = np.zeros(4)
for n in range(2, 6):
    INFTY = 1000000
    possible_times = np.array([1, 3, 5, 7, 9])
    failure_times = np.zeros(100)
    machines = np.zeros(100)
    for i in range(100):
        s = n
        area = 0
        clock = 0
        s_last = n
        t_last = 0
        next_failure = np.random.choice(possible_times)
        repairs = np.array([INFTY])
        next_repair = INFTY

        while s != 0:
            event = timer()
            if event == 'f':
                failure()
            elif event == 'r':
                repair()
        failure_times[i] = clock
        machines[i] = area/clock
    
    avg_failure_times[n-2] = np.average(failure_times)
    avg_machines[n-2] = np.average(machines)
    if n == 5:
        sd = np.std(failure_times)
    
print("Average failure times for n = 2,3,4,5:", avg_failure_times)
print("Average number of machines for n = 2,3,4,5:", avg_machines)
print("The average and SD of time to failure of 5 machines are:", np.average(failure_times), "and", sd, "days")

plt.plot(avg_machines, avg_failure_times)
plt.xlabel("Average number of machines")
plt.ylabel("Average time to failure")
plt.show()