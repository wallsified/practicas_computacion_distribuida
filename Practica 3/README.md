# Práctica 3: Algoritmos en Computación Distribuida

| Alumno                        | No. Cuenta |
|-------------------------------|------------|
| Paredes Zamudio Luis Daniel   | 318159926  |
| Reyna Mendez Cristian Ignacio | 320149579  |
| Lopez Ramirez Juan Carlos     | 316186021  |

# Ejecución

```bash
- Abrir el archivo …/Practica 3/src
- Instalar mediante terminar simpy -> pip install simpy
- Correr con el comando -> pytest -q Test.py
```

# Implementación

## NodoBFS.py

Para nuestro algoritmo BFS, hemos realizado estas adecuaciones y serie de pasos para la programación.
- El nodo distinguido (ID 0) arranca el proceso enviándose un mensaje GO a sí mismo.
- Cuando un nodo es visitado por primera vez por un GO, establece su padre y distancia. Luego, reenvía el GO a todos sus vecinos (excepto a su padre) y espera una respuesta de cada uno, usando un contador expected_msg.
- Los nodos responden con un BACK. Cuando un nodo ha recibido todos los BACK que esperaba (expected_msg llega a 0), confirma a su propio padre con otro BACK.
- El proceso termina cuando el nodo distinguido ha recibido todas las confirmaciones.
  
## NodoDFS.py

Para nuestro algoritmo DFS, hemos seguido está serie de pasos.
- El nodo distinguido (ID 0) inicia la exploración enviando un GO a su vecino con el menor ID.
- Al recibir el GO, un nodo se añade a la lista de visitados y pasa el GO a su siguiente vecino no visitado de menor ID. 
- Cuando el nodo receptor no encuentra vecinos no visitados envía BACK a su padre. El padre, al recibirlo:
	- Envía el GO por la del vecino con menor ID. Esto si hay algún vecino no visitado.
	 - Caso contrario, manda BACK a su padre.
- El algoritmo termina cuando BACK regresa al nodo distinguido y este ya no tiene nodos no visitados.

