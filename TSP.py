"""""
            ### Traveling Salesman Problem, TSP ###

The goal is to find the shortest route that allows a salesperson 
to visit all the cities of a set once and return to the city 
of departure.


                        ### Formula ###

### 1 Each city is visited only once

### 2 The route must form a cycle: the salesman must return to 
###   the city of departure.

### 3 Total distance minimization: 
      The goal is to reduce the total distance traveled in the cycle.

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

# number of nodes
n_city = len(distances)

# Solver
opt = Optimize()

# Variables: Each city occupies a different position in the route
city = [Int(f'city_{i}') for i in range(n_city)]

# Constraints (1): Each city must be visited exactly once
opt.add([And(city[i] >=0, city[i] < n_city)
            for i in range(n_city)])

# Constraint (2): All cities must be different
opt.add(Distinct(city))

# Objective function:
# total distance calculated with additional constraints
distance_vars = []
for i in range(n_city):

    # Symbolic variable's def for
    # the distance between two consecutive cities
    dist = Int(f'dist_{i}')
    distance_vars.append(dist)

    # Constraint for the variable 'dist': must represent
    # the distance between city[i] and city[(i + 1) % n_city]
    opt.add(Or([And(city[i] == a, city[(i+1) % n_city] == b,
                    dist == distances[a][b]) for a in range(n_city)
                for b in range(n_city)]))

# Minimization of total distance
total_distance = Sum(distance_vars)
opt.minimize(total_distance)


# Let's find the solution
if opt.check() == sat:
    model = opt.model()

    # Variable evaluation to obtain the optimal path in integers
    path = [model.evaluate(city[i]).as_long() for i in range(n_city)]

    # Total distance calculation
    calc_distance = sum(distances[path[i]][path[(i+1) % n_city]]
                        for i in range(n_city))

    print("Shortest route: ", path) # Shortest route:  [1, 3, 4, 2, 0]
    print("Total distance: ", calc_distance) # Total distance:  85
else:
    print("No solution found!")













