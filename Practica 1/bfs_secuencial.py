from collections import deque  # se usa deque para usar queue eficientemente

"""
Implementación de Breadth-First Search (BFS) para una gráfica conexa. 
El algoritmo explora todos los vecinos de un nodo antes de moverse a los nodos en el siguiente nivel.
"""


def bfs(grafica, inicio):
    # Lista para rastrear nodos visitados
    visitados = []
    # Se inicia la cola con el nodo inicial especificado.
    queue = deque([inicio])

    while queue:  # Mientras aún haya nodos en la cola
        nodo = queue.popleft()  # Se saca el primer nodo de la cola.

        if nodo not in visitados:  # Se revisa si el nodo ya fue visitado.
            visitados.append(nodo)  # Caso contrario, se marca como visitado.
            print(nodo, end=" ")

            # Se agregan los vecinos del nodo a la cola.
            for vecino in grafica[nodo]:
                if vecino not in visitados:
                    queue.append(vecino)


# El patrón es que cada nodo apunta a una lista de sus vecinos.
# Esta es una gráfica de ejemplo.
graficaA = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['H', 'I'],
    'E': ['J', 'K'],
    'F': ['L', 'M'],
    'G': ['N', 'O'],
    'H': [], 'I': [], 'J': [], 'K': [],
    'L': [], 'M': [], 'N': [], 'O': []
}

bfs(graficaA, "A")
