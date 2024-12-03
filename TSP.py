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

def tsp(cities, distances):
    """
    Solves the Traveling Salesman Problem (TSP) for a set of cities and a distance matrix using Z3 arrays.

    Args:
        cities (list): A list of city names.
        distances (list of lists): A matrix representing distances between cities.

    Returns:
        tuple: A sequence of cities representing the shortest path and its total distance if a solution exists.
        None: If no solution is found.
    """
    
    # Number of cities
    n_city = len(cities)

    # Create an optimization solver
    opt = Optimize()

    # Define a symbolic array to represent the sequence of cities in the path
    path = Array('path', IntSort(), IntSort())

    # Constraint (1): Each city must be visited exactly once
    # Create a list of boolean variables to track whether each city has been visited
    visited = [Bool(f'visited_{i}') for i in range(n_city)]
    for i in range(n_city):
        # Add a constraint to ensure each city appears at least once in the path
        opt.add(Or([path[j] == i for j in range(n_city)]))
        # Connect the visited status to the path
        opt.add(visited[i] == Or([path[j] == i for j in range(n_city)]))

    # Constraint (2): The positions in the path must be distinct
    for i in range(n_city):
        for j in range(i + 1, n_city):
            # Ensure no two positions in the path contain the same city
            opt.add(path[i] != path[j])

    # Define variables to store the distances between consecutive cities in the path
    distance_vars = [Int(f'dist_{i}') for i in range(n_city)]
    for i in range(n_city):
        # Add constraints to associate distance variables with the distances in the matrix
        opt.add(Or([
            And(path[i] == a, path[(i + 1) % n_city] == b, distance_vars[i] == distances[a][b])
            for a in range(n_city) for b in range(n_city)
        ]))

    # Objective function: Minimize the total distance of the path
    total_distance = Sum(distance_vars)
    opt.minimize(total_distance)

    # Solve the problem
    if opt.check() == sat:
        # If a solution exists, retrieve the model
        model = opt.model()

        # Extract the path by evaluating the symbolic array
        path_eval = [model.evaluate(path[i]).as_long() for i in range(n_city)]

        # Calculate the total distance based on the solution
        calc_distance = sum(distances[path_eval[i]][path_eval[(i + 1) % n_city]] for i in range(n_city))

        return path_eval, calc_distance
    else:
        # Return None if no solution is found
        return None, None


# Example usage
if __name__ == "__main__":
    # Define the cities (e.g., 5 cities)
    cities = ["Roma", "Milano", "Firenze", "Napoli", "Venezia"]

    # Distance matrix representing the distances between each pair of cities
    distances = [
        [0, 10, 15, 20, 25],
        [10, 0, 35, 25, 30],
        [15, 35, 0, 30, 20],
        [20, 25, 30, 0, 15],
        [25, 30, 20, 15, 0]
    ]

    # Solve for the shortest path
    path, total_distance = tsp(cities, distances)

    if path:
        # If a solution is found, print the path and its total distance
        print("Il cammino più breve: ", [cities[i] for i in path])
        print("Distanza totale: ", total_distance)
    else:
        # If no solution exists, print an appropriate message
        print("Nessuna soluzione trovata!")
