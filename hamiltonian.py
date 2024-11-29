from z3 import *
import time  # Importa il modulo per misurare il tempo

def hamiltonian_path(cities, graph, n):
    """
    Risolve il problema del cammino Hamiltoniano per un grafo dato di città.

    Args:
        cities (list): Lista di città etichettate da 0 a n-1.
        graph (list of tuples): Lista di archi (u, v) che rappresentano il grafo delle città.
        n (int): Numero di città nel grafo.

    Returns:
        list: Una sequenza di città che rappresenta il cammino Hamiltoniano, se esiste.
        None: Se il cammino non esiste.
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
        # Restituisci il cammino delle città (in ordine)
        execution_time = time.time() - start_time  # Calcola il tempo di esecuzione
        return [cities[i] for i in path], execution_time
    else:
        execution_time = time.time() - start_time  # Calcola il tempo di esecuzione
        return None, execution_time

# Esempio di utilizzo
if __name__ == "__main__":
    # Definizione delle città (in questo caso 5 città)
    cities = ["Roma", "Milano", "Firenze", "Napoli", "Venezia"]

    # Definizione del grafo come lista di archi (le connessioni tra le città)
    graph = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0),  # Connessioni cicliche
             (0, 2), (1, 3), (2, 4), (0, 3), (1, 4)]  # Connessioni aggiuntive

    # Numero di città
    n = len(cities)

    # Trova il cammino Hamiltoniano
    result, execution_time = hamiltonian_path(cities, graph, n)

    if result:
        print("Cammino Hamiltoniano trovato:", result)
    else:
        print("Nessun cammino Hamiltoniano trovato.")
    
    print(f"Tempo di esecuzione del solver: {execution_time:.4f} secondi")
