from z3 import *
import time  # Importa il modulo per misurare il tempo
import random


def hamiltonian_path(cities, graph, n, timeout_ms=5000):
    """
    Risolve il problema del cammino Hamiltoniano per un grafo dato di città con un timeout.

    Args:
        cities (list): Lista di città etichettate da 0 a n-1.
        graph (list of tuples): Lista di archi (u, v) che rappresentano il grafo delle città.
        n (int): Numero di città nel grafo.
        timeout_ms (int): Timeout in millisecondi (default 5000 ms = 5 secondi).

    Returns:
        tuple: Una tupla contenente la sequenza di città che rappresenta il cammino Hamiltoniano e il tempo di esecuzione, se esiste.
        None: Se il cammino non esiste o se si verifica un timeout.
    """
    # Crea un Solver con il timeout
    s = Solver()
    s.set("timeout", timeout_ms)  # Imposta il timeout in millisecondi

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
    result = None
    try:
        if s.check() == sat:
            model = s.model()
            path = [model.eval(position[i]).as_long() for i in range(n)]
            execution_time = time.time() - start_time  # Calcola il tempo di esecuzione
            result = (path, execution_time)
        else:
            execution_time = time.time() - start_time  # Calcola il tempo di esecuzione
            result = (None, execution_time)
    except Z3Exception:
        # Gestisci il caso in cui Z3 non riesca a risolvere il problema entro il timeout
        execution_time = time.time() - start_time
        result = (None, execution_time)

    return result


# Esempio di utilizzo
if __name__ == "__main__":
    # Numero di città
    n = 100

    # Crea l'array cities
    cities = [f"City_{i}" for i in range(n)]

    # Crea l'array graph con le connessioni
    graph = []

    # Aggiungi le connessioni cicliche (ogni città connessa alla successiva, ultima con la prima)
    for i in range(n):
        graph.append((i, (i + 1) % n))  # Connessione tra la città i e la città (i+1)%n (ciclo)

    # Aggiungi connessioni casuali tra alcune città per esempio
    for _ in range(n // 10):  # Aggiungi circa un decimo delle città con connessioni casuali
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and (u, v) not in graph and (v, u) not in graph:  # Assicurati che la connessione non esista già
            graph.append((u, v))

    # Trova il cammino Hamiltoniano con un timeout di 5 secondi
    result = hamiltonian_path(cities, graph, n, timeout_ms=5000)

    # Controlla se il risultato è valido
    if result and result[0]:
        print("Cammino Hamiltoniano trovato:", result[0])
    else:
        print("Nessun cammino Hamiltoniano trovato.")

    print(
        f"Tempo di esecuzione del solver: {result[1]:.4f} secondi" if result else "Errore durante l'esecuzione del solver.")
