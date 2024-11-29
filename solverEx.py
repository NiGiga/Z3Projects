from z3 import *

x = Int('x')
y = Int('y')

s = Solver()
s.add(x + y == 10, x > 0, y > 0)

print("Vincoli:", s.assertions())
if s.check() == sat:
    print("Soddisfacibile!")
    print("Modello:", s.model())
else:
    print("Non soddisfacibile!")
