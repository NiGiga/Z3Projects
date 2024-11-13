"""
Goal: solve the following problem

square * square + circle = 16
triangle * triangle * triangle = 27
triangle * square = 6
square * circle * triangle = ?

"""

# library for z3
from z3 import *

#define unknown values using Int()
square = Int('square')
circle = Int('circle')
triangle = Int('triangle')

# define Solver()
solver = Solver()

# adding the constraints
solver.add(square * square + circle == 16)
solver.add(triangle * triangle * triangle == 27)
solver.add(triangle * square == 6)

# Let's check the satisfiability
if solver.check() == sat:
    model = solver.model()

    #convert to int
    circle_val = model.eval(circle).as_long()
    triangle_val = model.eval(triangle).as_long()
    square_val = model.eval(square).as_long()

    # simple arithmetic
    result = square_val * circle_val * triangle_val

    print(model) #[circle = 12, triangle = 3, square = 2]
    print(result) #72
