from z3 import Optimize, Int

opt = Optimize()

# Definisci le variabili
x = Int('x')from z3 import Optimize, Int

opt = Optimize()

# Definisci le variabili
x = Int('x')
y = Int('y')

# Aggiungi i vincoli
opt.add(x > 0, y > 0)

# Prima ottimizza x (minimizza il costo)
opt.minimize(x)

# Poi ottimizza y (minimizza la distanza)
opt.minimize(y)

# Risolvi
if opt.check() == sat:
    model = opt.model()
    print("Optimal solution:", model)
y = Int('y')

# Aggiungi i vincoli
opt.add(x > 0, y > 0)

# Prima ottimizza x (minimizza il costo)
opt.minimize(x)

# Poi ottimizza y (minimizza la distanza)
opt.minimize(y)

# Risolvi
if opt.check() == sat:
    model = opt.model()
    print("Optimal solution:", model)
