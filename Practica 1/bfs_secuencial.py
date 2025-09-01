import argparse
import json
from collections import deque  # se usa deque para usar queue eficientemente

"""
Implementación de Breadth-First Search (BFS) para una gráfica conexa. 
El algoritmo explora todos los vecinos de un nodo antes de moverse a los nodos en el siguiente nivel.
Alumnos:
- Paredes Zamudio Luis Daniel, 318159926
- Reyna Mendez Cristian Ignacio, 320149579
- Lopez Ramirez Juan Carlos, 316186021
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="bfs_secuencial.py",
                                     description="BFS en una gráfica conexa.",
                                     epilog="Usa --help para más información.")
    parser.add_argument("--grafica", type=str, help="Gráfica en formato JSON. Pon la ruta del archivo entre comillas.")
    parser.add_argument("--inicio", type=str, help="Nodo inicial para BFS. Pon el nodo entre comillas.")
    args = parser.parse_args()

    if args.grafica and args.inicio:
        # Suponemos un archivo json para ingresar la gráfica.
        try:
            with open(args.grafica, "r") as archivo:
                grafica = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error al leer la gráfica: {e}")
            exit(1)

        if args.inicio not in grafica:
            print(f"El nodo inicial '{args.inicio}' no está en la gráfica.")
            exit(1)

        bfs(grafica, args.inicio)

    else:
        print("Por favor, proporciona tanto la gráfica como el nodo inicial.")
        parser.print_help()

# El patrón es que cada nodo apunta a una lista de sus vecinos.
# Esta es la misma gráfica en gráfica.json
# graficaA = {
#    'A': ['B', 'C'],
#    'B': ['D', 'E'],
#    'C': ['F', 'G'],
#    'D': ['H', 'I'],
#    'E': ['J', 'K'],
#    'F': ['L', 'M'],
#    'G': ['N', 'O'],
#    'H': [], 'I': [], 'J': [], 'K': [],
#    'L': [], 'M': [], 'N': [], 'O': []
# }
