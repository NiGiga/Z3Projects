"""""
            ### Traveling Salesman Problem plus, TSP+ ###

Extension of the Salesman problem by introducing additional 
constraints and objectives.
Capacity constraints: Imagine that every city has a demand 
for resources and that the salesperson has a maximum capacity 
of resources to transport. 
Time window: Each city can only be visited in certain time frames. 
Supply Points: The clerk must visit certain cities to recharge 
resource capacity before visiting other cities. 
Multiple salespeople: Let's consider multiple salespeople 
who have to cover different parts of the journey.


                        ### Formula ###

### 1 The salesperson has a maximum capacity of resources that he can carry.

### 2 Every city has a demand for resources that must be met.

### 3 Each city can only be visited in a certain time frame.

### 4 The route must minimize the total distance, respect the capacity and visit each city within its time window.


                          ### Idea ###
                          
I define a simplified version with a matrix of distances between 
cities, using variables to represent the sequence of cities visited.

"""""

from z3 import *

# Distances between 5 cities, defined in a symmetric matrix
distances = [
    [0, 10, 15, 20, 25],
    [10, 0, 35, 25, 30],
    [15, 35, 0, 30, 20],
    [20, 25, 30, 0, 15],
    [25, 30, 20, 15, 0]
]

# Number of nodes
n_city = len(distances)

# Maximum salesperson capacity and resource requirements for each city
capacity = 40
demands = [0, 10, 15, 20, 10]  # The first city (0) has request zero

# Time window for each city (min and max "time" to spend)
time_windows = [(0, 10), (2, 6), (3, 8), (1, 7), (4, 9)]

# Let's make the optimizer
opt = Optimize()

# Variables: each city occupies a position in the route and a visit time
city = [Int(f'city_{i}') for i in range(n_city)]
visit_time = [Int(f'visit_time_{i}') for i in range(n_city)]

# Constraints on the location and distinction of cities in the route
opt.add([And(city[i] >= 0, city[i] < n_city) for i in range(n_city)])
opt.add(Distinct(city))

# Capacity constraints: the clerk must not exceed the capacity carried
load_vars = []
for i in range(n_city):
    load_var = Int(f'load_{i}')
    load_vars.append(load_var)
    # Cumulative load up to each city
    opt.add(load_var == Sum([If(city[j] == i, demands[j], 0) for j in range(n_city)]))
    opt.add(load_var <= capacity)  # Capacity constraint

# Time window constraints: each city must be visited within its range
for i in range(n_city):
    min_time, max_time = time_windows[i]
    opt.add(visit_time[i] >= min_time)
    opt.add(visit_time[i] <= max_time)

# Objective function: total distance calculated with additional constraints
distance_vars = []
for i in range(n_city):
    dist = Int(f'dist_{i}')
    distance_vars.append(dist)
    opt.add(Or([And(city[i] == a, city[(i + 1) % n_city] == b, dist == distances[a][b])
                for a in range(n_city) for b in range(n_city)]))

# Minimization of total distance
total_distance = Sum(distance_vars)
opt.minimize(total_distance)

# Let's find the solution
if opt.check() == sat:
    model = opt.model()

    # Variable evaluation to obtain the optimal path, time, load in integers
    path = [model.evaluate(city[i]).as_long() for i in range(n_city)]
    times = [model.evaluate(visit_time[i]).as_long() for i in range(n_city)]
    load_vals = [model.evaluate(load_vars[i]).as_long() for i in range(n_city)]
    # Total distance calculation
    calc_distance = sum(distances[path[i]][path[(i + 1) % n_city]]
                        for i in range(n_city))

    print("Shortest route:", path) # Shortest route: [1, 3, 4, 2, 0]
    print("Time windows:", times) # Time windows: [0, 2, 3, 1, 4]
    print("Transported cargo:", load_vals) # Transported cargo: [10, 0, 20, 10, 15]
    print("Total distance:", calc_distance) # Total distance: 85

else:
    print("No solution found!")
