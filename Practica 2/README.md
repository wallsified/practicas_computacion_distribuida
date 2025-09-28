# Práctica 2: Algoritmos en Computación Distribuida

| Alumno                        | No. Cuenta |
|-------------------------------|------------|
| Paredes Zamudio Luis Daniel   | 318159926  |
| Reyna Mendez Cristian Ignacio | 320149579  |
| Lopez Ramirez Juan Carlos     | 316186021  |

# Ejecución

```bash
python3 -m venv ./venv
source venv/bin/activate
pip install simpy pytest
pytest test.py
```

# Conocimientos Previos:

- Nodo.py define la estructura básica de un nodo en la red, incluyendo su identificador, vecinos y canales de comunicación. 
- Canal.py es una interfaz que modela el comportamiento de los canales de mensajes entre nodos
- CanalBroadcast.py implementa un canal que permite enviar mensajes a múltiples nodos simultáneamente. Estas clases facilitan la simulación de algoritmos distribuidos al abstraer la comunicación entre procesos.

# Implementación

## NodoVecinos.py

NodoVecinos permite que cada nodo en la gráfica descubra los vecinos de sus propios vecinos en la gráfica (o en la red), envíando su lista de vecinos a todos sus vecinos utilizando el canal de salida. Luego, espera recibir por su canal de entrada las listas de vecinos enviadas por los demás nodos. Conforme recibe estas listas, acumula los IDS en _identifiers_, y así se conocen los nodos de segundo nivel en la topología de la gráfica.

Aquí partimos de un ID de cada Nodo, una lista de vecinos, un canal de entrada y otro de salida y un conjunto de IDs para guardar los identificadores de los vecinos de los vecinos.

## NodoGenedor.py

Partimos de un ID, una lista de vecinos y de hijos, un canal de entrada y de salida y un indicador de mensajes esperados, esto para cada Nodo. Luego, sucede lo siguiente:

- Se crea el entorno de simulación y los nodos, asignando sus vecinos y canales de comunicación.
- El nodo distinguido (ID 0) inicia el proceso enviando mensajes "GO" a sus vecinos.
- Cada nodo, al recibir un "GO" por primera vez, fija al remitente como padre y propaga "GO" al resto de sus vecinos.
- Los nodos esperan recibir mensajes "BACK" de sus hijos potenciales.
- Al recibir todos los "BACK", cada nodo responde a su padre, indicando si forma parte del árbol.
- El proceso continúa hasta que todos los nodos han respondido y el árbol queda construido. 

Ocupamos la función auxiliar _get\_vecino\_por\_id_ para iterar entre la lista de vecinos y encontrar el que corresponde al ID buscado al momento de mandar _BACK()_

## NodoBroadcast.py

Aqui buscamos simular el proceso de Broadcast. Partimos de un ID, una lista de vecinos, un canal de entrada y de salida, un mensaje a enviar y una lista para mapear los Ids a otros nodos, esto para cada Nodo. Luego, sucede lo siguiente:

1. Se inicializan los nodos y canales en el entorno de simulación.
2. El nodo con ID 0 inicia el broadcast enviando el mensaje a todos sus vecinos, partiendo de que ya se envio el mensaje a si mismo.
3. Cada nodo espera recibir mensajes en su canal de entrada.
4. Al recibir un mensaje de tipo "GO", el nodo lo reenvía a todos sus vecinos.
5. El proceso continúa hasta que el mensaje ha sido propagado por toda la red.

Aquí no buscamos regresar algo, solo ampliar el alcance del mensaje.