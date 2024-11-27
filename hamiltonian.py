from z3 import *

def hamiltonian_path(graph, n):
    """
    Solves the Hamiltonian Path problem for a given graph.

    Args:
        graph (list of tuples): List of edges (u, v) representing the graph.
        n (int): Number of nodes in the graph.

    Returns:
        list: A sequence of nodes representing the Hamiltonian path, if it exists.
        None: If no Hamiltonian path exists.
    """
    # Create a Z3 Solver
    s = Solver()

    # Decision variables: position[i] represents the node at position i in the path
    position = [Int(f'pos_{i}') for i in range(n)]

    # Constraint 1: Each position must contain a valid node (between 0 and n-1)
    s.add([And(position[i] >= 0, position[i] < n) for i in range(n)])

    # Constraint 2: All nodes in the path must be distinct (no repetition)
    s.add(Distinct(position))

    # Constraint 3: Consecutive nodes in the path must be connected by an edge
    edge_set = set(graph)  # Use a set for efficient lookup
    for i in range(n - 1):
        u = position[i]
        v = position[i + 1]
        # Ensure that (u, v) or (v, u) is a valid edge in the graph
        s.add(Or([And(u == e[0], v == e[1]) for e in edge_set] +
                 [And(u == e[1], v == e[0]) for e in edge_set]))

    # Solve the problem
    if s.check() == sat:
        model = s.model()  # Extract the solution model
        # Extract the path from the model as a list of integers
        path = [model.eval(position[i]).as_long() for i in range(n)]
        return path
    else:
        return None  # No Hamiltonian path found

# Example usage
if __name__ == "__main__":
    # Define the graph as a list of edges
    graph = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3)]
    n = 4  # Number of nodes in the graph

    # Find the Hamiltonian path
    result = hamiltonian_path(graph, n)

    if result:
        print("Hamiltonian Path found:", result)
    else:
        print("No Hamiltonian Path exists.")
