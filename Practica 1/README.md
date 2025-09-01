# Práctica 1: BFS en un Gráfica Conexa

| Alumno                        | No. Cuenta |
|-------------------------------|------------|
| Paredes Zamudio Luis Daniel   | 318159926  |
| Reyna Mendez Cristian Ignacio | 320149579  |
| Lopez Ramirez Juan Carlos     | 316186021  |

El script **bfs_secuencial.py** implementa el algoritmo de búsqueda en anchura (BFS) para recorrer una gráfica conexa.
Recibe dos parámetros por línea de comandos: la ruta de un archivo JSON que contiene la gráfica
y el nodo inicial desde el cual comienza la búsqueda.

El script valída que el archivo y el formato sean correctos, y que el nodo inicial exista en la gráfica.
Luego imprime el recorrido BFS desde el nodo indicado.

## Funcionamiento

BFS explora los nodos de la gráfica en niveles, comenzando desde el nodo inicial ingresado.
Utiliza una cola para mantener el orden de los nodos a visitar y un conjunto para rastrear los nodos ya visitados,
asegurando que cada nodo se procese una sola vez. Al final del recorrido, se imprime la secuencia de nodos visitados.

## Ejecución

El script realiza la búsqueda sobre una gráfica representada en formato JSON.
Para ejecutarlo, se debe proporcionar la ruta al archivo JSON de la gráfica y el nodo
inicial desde el cual se inicia la búsqueda. Por ejemplo:

```bash
python bfs_secuencial.py --grafica "grafica.json" --inicio "A"
```

Se incluye una gráfica de ejemplo en el archivo `grafica.json`, la cual tiene la siguiente estructura:

```json
{
  "A": [
    "B",
    "C"
  ],
  "B": [
    "A",
    "D",
    "E"
  ],
  "C": [
    "A",
    "F"
  ],
  "D": [
    "B"
  ],
  "E": [
    "B",
    "F"
  ],
  "F": [
    "C",
    "E"
  ]
}
```

donde cada clave representa un nodo y su valor es una lista de nodos adyacentes.