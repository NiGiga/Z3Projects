from z3 import *
import time  # Importa il modulo per misurare il tempo
import random

def hamiltonian_path(cities, graph, n):
    """
    Risolve il problema del cammino Hamiltoniano per un grafo dato di città.

    Args:
        cities (list): Lista di città etichettate da 0 a n-1.
        graph (list of tuples): Lista di archi (u, v) che rappresentano il grafo delle città.
        n (int): Numero di città nel grafo.

    Returns:
        tuple: Una tupla contenente la sequenza di città che rappresenta il cammino Hamiltoniano e il tempo di esecuzione, se esiste.
        tuple: (None, execution_time) se il cammino non esiste.
    """
    # Crea un Solver
    s = Solver()

    # Variabili di decisione: posizione[i] è la città nella posizione i del cammino
    position = [Int(f'pos_{i}') for i in range(n)]

    # Ogni posizione deve contenere una città valida (da 0 a n-1)
    s.add([And(position[i] >= 0, position[i] < n) for i in range(n)])

    # Le città nel cammino devono essere tutte diverse
    s.add(Distinct(position))

    # Collegamenti tra città: ogni città i deve essere connessa alla città i+1 nel cammino
    edge_set = set(graph)  # Usa un set per un accesso rapido
    for i in range(n - 1):
        u = position[i]
        v = position[i + 1]
        s.add(Or([And(u == e[0], v == e[1]) for e in edge_set] +
                 [And(u == e[1], v == e[0]) for e in edge_set]))

    # Inizia a misurare il tempo di esecuzione
    start_time = time.time()

    # Risolvi il problema
    if s.check() == sat:
        model = s.model()
        path = [model.eval(position[i]).as_long() for i in range(n)]
        execution_time = time.time() - start_time  # Calcola il tempo di esecuzione
        return path, execution_time  # Restituisci sia il cammino che il tempo
    else:
        execution_time = time.time() - start_time  # Calcola il tempo di esecuzione
        return None, execution_time  # Restituisci None e il tempo

# Esempio di utilizzo
if __name__ == "__main__":
    # Numero di città
    n = 200

    # Crea l'array cities
    cities = [f"City_{i}" for i in range(n)]

    # Crea l'array graph con le connessioni
    graph = []

    # Aggiungi le connessioni cicliche (ogni città connessa alla successiva, ultima con la prima)
    for i in range(n):
        graph.append((i, (i + 1) % n))  # Connessione tra la città i e la città (i+1)%n (ciclo)

    # Aggiungi connessioni casuali tra alcune città
    for _ in range(n // 10):  # Aggiungi circa un decimo delle città con connessioni casuali
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and (u, v) not in graph and (v, u) not in graph:  # Assicurati che la connessione non esista già
            graph.append((u, v))

    # Trova il cammino Hamiltoniano
    result, execution_time = hamiltonian_path(cities, graph, n)

    if result:
        print("Cammino Hamiltoniano trovato:", result)
    else:
        print("Nessun cammino Hamiltoniano trovato.")

    print(f"Tempo di esecuzione del solver: {execution_time:.4f} secondi")
