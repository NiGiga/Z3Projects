from z3 import *

# Dichiarazione delle variabili proposizionali
p, q, r = Bools('p q r')

# Definizione della formula
formula = And(Or(p, q),       # p ∨ q
              Or(Not(p), r),  # ¬p ∨ r
              Or(Not(q), Not(r)))  # ¬q ∨ ¬r

# Creazione del solver
solver = Solver()
solver.add(formula)

# Verifica della soddisfacibilità
if solver.check() == sat:
    print("La formula è soddisfacibile.")
    print("Esempio di modello che la soddisfa:", solver.model())
else:
    print("La formula non è soddisfacibile.")
