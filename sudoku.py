"""""
                        ### Sudoku Problem ###

Write a 4x4 Sudoku solver using Z3. 
The goal is to find a valid Sudoku setup where each number 
from 1 to 4 appears only once in each row, column, and 2x2 sub-block.


                        ### Formula ###

### 1 Each cell C[i][j](where i is the row and j is the column)
      contains a number from 1 to 4

### 2 Each number appears only once in each row and column.

### 3 Each number appears only once in each 2x2 sub-block.

"""""

from z3 import *

# Variables (defined by function Int()): A 4x4 matrix of integers
C = [[Int("C_%d_%d" % (i,j)) for j in range(4)] for i in range(4)]

# Constraints (1): Each cell must contain a number between 1 and 4
cells = [And(1<= C[i][j], C[i][j]<=4)for i in range(4)for j in range(4)]

# Constraints (2): Each row must contain unique numbers
rows = [Distinct(C[i]) for i in range(4)]

# Constraints (2): Each column must contain unique numbers
cols = [Distinct([C[i][j] for i in range(4)]) for j in range(4)]

# Constraints (3): Each 2x2 block must contain unique numbers
blocks = [Distinct([C[i][j] for i in range(2 * r, 2 * r + 2) for j in range(2 * c, 2* c + 2)])
          for r in range(2) for c in range(2)]

# Let's create the solver and add all the constraints
s = Solver()
s.add(cells + rows + cols + blocks)

# Let's check the satisfiability
if s.check() == sat:
    m = s.model()
    result = [[m.evaluate(C[i][j]) for j in range(4)] for i in range(4)]
    for row in result:
        print(row)
else:
    print("No solution found!")