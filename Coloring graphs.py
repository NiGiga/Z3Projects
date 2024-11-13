"""""
                ### Coloring graphs Problem ###

Let's consider a simple graph with 5 nodes and some edges: 
you want to find a color with 3 colors (colors represented 
by integers 1, 2 and 3) where nodes connected by an edge have 
different colors.


                        ### Formula ###

### 1 Each node has a color from 1 to 3.

### 2 Two nodes connected by an arc do not have to have the same color.

"""""

from z3 import *

# We define nodes as integer variables
nodes = [Int("node_%d" % i)for i in range(5)]

# Let's define the arcs (example)
edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]

# Constraints (1): Each node has a color from 1 to 3
colors = [And(1 <= node, node <= 3) for node in nodes]

# Constraints (2): Nodes connected by an arc must have different colors
adj_constraints = [nodes[u] != nodes[v] for u,v in edges]

# Let's create the solver and add the constraints
s = Solver()
s.add(colors + adj_constraints)

# Let's check the satisfiability
if s.check() == sat:
    m = s.model()
    result = [m.evaluate(nodes[i]) for i in range(5)]
    print("Coloring found:", result) # Coloring found: [1, 2, 1, 2, 3]
else:
    print("No coloring found!")