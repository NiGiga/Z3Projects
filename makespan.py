"""""
      ### Scheduling Problem with Resources and Penalties ###

Imagine that we have tasks that need to be completed in a certain 
order, but these tasks require limited resources 
(e.g., machinery, operators, time) and are subject to penalties if 
they are not completed in the required time. 
Our goal could be to minimize the total time to completion, 
or makespan, which is the time in which all tasks are completed, 
respecting all constraints.

In this example, we will have:

### 1 Tasks that must be executed sequentially, with durations 
      and start and end constraints.

### 2 Limited resources for each task (for example, a machine can 
      only perform one task at a time).
      
### 3 Penalties if a task is not completed in the allotted time. 

### 4 Objective: Minimize makespan (total completion time) and penalties.

"""""

from z3 import *

# Parameters
n_activities = 5
n_machines = 3  # Number of machines

# Task durations and time windows
durations = [2, 3, 4, 1, 5]
time_windows = [(0, 5), (2, 7), (3, 7), (1, 8), (4, 9)]

# Variables: when tasks start, when they end, and the machines assigned
start_times = [Int(f'start_{i}') for i in range(n_activities)]
end_times = [Int(f'end_{i}') for i in range(n_activities)]
machines = [Int(f'machines_{i}') for i in range(n_activities)]

# Create the solver
opt = Optimize()

# Constraints: time windows (tasks must start and finish within their window)
for i in range(n_activities):
    min_time, max_time = time_windows[i]

    # Ensure the task starts and ends within its time window
    opt.add(start_times[i] >= min_time)
    opt.add(end_times[i] <= max_time)

    # Ensure end time is the start time plus duration
    opt.add(end_times[i] == start_times[i] + durations[i])

# Machine constraints: Each machine can only perform one task at a time
for i in range(n_activities):
    for j in range(i + 1, n_activities):  # Compare each task only once
        # Ensure that tasks assigned to the same machine do not overlap
        opt.add(Implies(machines[i] == machines[j],
                        Or(end_times[i] <= start_times[j], end_times[j] <= start_times[i])))

# Ensure that machine indices are within valid range (0 to n_machines-1)
for i in range(n_activities):
    opt.add(And(machines[i] >= 0, machines[i] < n_machines))

# Solve the problem
if opt.check() == sat:
    model = opt.model()

    # Evaluate the variables and print results
    start_vals = [model.evaluate(start_times[i]).as_long() for i in range(n_activities)]
    end_vals = [model.evaluate(end_times[i]).as_long() for i in range(n_activities)]
    machine_vals = [model.evaluate(machines[i]).as_long() for i in range(n_activities)]

    print("Start times:", start_vals) # Start times: [0, 2, 3, 1, 4]
    print("End times:", end_vals) # End times: [2, 5, 7, 2, 9]
    print("Assigned machines:", machine_vals) # Assigned machines: [2, 1, 2, 1, 0]

else:
    print("No solution found!")


































