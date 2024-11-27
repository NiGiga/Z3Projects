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

# Solver
solver = Solver()

# Variables: Each city occupies a different position in the path
city = [Int(f'city_{i}') for i in range(n_city)]

# Constraints (1): Each city must be visited exactly once
solver.add([And(city[i] >= 0, city[i] < n_city) for i in range(n_city)])

# Constraint (2): All cities must be distinct
solver.add(Distinct(city))

# Constraint (3): Consecutive cities must be connected (non-infinite distance)
for i in range(n_city - 1):  # No cyclic condition here
    solver.add(Or([And(city[i] == a, city[i + 1] == b,
                       distances[a][b] > 0) for a in range(n_city)
                   for b in range(n_city)]))

# Solve the problem
if solver.check() == sat:
    model = solver.model()

    # Variable evaluation to obtain the path
    path = [model.evaluate(city[i]).as_long() for i in range(n_city)]

    # Total distance calculation
    calc_distance = sum(distances[path[i]][path[i + 1]] for i in range(n_city - 1))

    print("Hamiltonian Path: ", path)  # Example: [0, 2, 4, 3, 1]
    print("Total distance: ", calc_distance)  # Example: 80
else:
    print("No Hamiltonian Path exists!")
