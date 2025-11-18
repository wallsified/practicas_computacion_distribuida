# Práctica 5: Relojes Lógicos

| Alumno                        | No. Cuenta |
|-------------------------------|------------|
| Paredes Zamudio Luis Daniel   | 318159926  |
| Reyna Mendez Cristian Ignacio | 320149579  |
| Lopez Ramirez Juan Carlos     | 316186021  |

> Nota:
> Para que el sistema sea parcialmente asíncrono usamos delays aleatorios (entre 0.1 y 0.5 segundos, si fuera más tiempo tardarían demasiado en ejecutarse) antes de cada envío y recepción de mensajes. 

# Resumen de implementación del Reloj de Lamport

El reloj de Lamport se implementa sobre el algoritmo de Broadcast usando un contador entero que mantiene el orden causal de los eventos. Cada nodo incrementa su reloj antes de enviar un mensaje y al recibir actualiza su reloj al máximo entre el reloj local y el recibido más uno. Todos los eventos (envíos y recepciones) se registran en una lista con el formato `[reloj, tipo, mensaje, emisor, receptor]`, donde el tipo es 'E' para envíos y 'R' para recepciones.

Recordemos que Broadcast funciona de la siguiente manera: 
- El nodo distinguido inicia enviando el mensaje a todos sus vecinos.
- Cada nodo que recibe un mensaje por primera vez lo reenvía a todos sus vecinos excepto al padre (quien se lo envió). 

Esto garantiza que el mensaje se propague por todo el árbol sin ciclos. 

Luego, los relojes de Lamport aseguran que cada par envío-recepción respete el orden causal, cumpliendo con la propiedad de que si un evento a ocurre antes que b, entonces el reloj de a es menor que el de b.

# Resumen de implementación del Reloj Vectorial

Para este caso, el reloj vectorial se implementa sobre el DFS usando un arreglo de enteros de tamaño `n` (con `n` el total de nodos en la gráfica). Aquí cada nodo mantiene su propio vector de relojes, donde la posición `i` representa el conocimiento que tiene el nodo sobre los eventos del nodo `i`. Al enviar un mensaje, el nodo incrementa su propia componente del vector y envía una copia del mismo. Luego, al recibir mensajes, cada nodo actualiza cada componente con el máximo entre su valor local y el recibido, y luego incrementa su propia componente.

Recordemos que DFS explora la gráfica en profundidad iniciando desde el nodo distinguido. Éste envía mensajes `GO` a sus vecinos no visitados (eligiendo siempre el de menor ID) y, cuando un nodo no puede avanzar más, envía `BACK` a su padre para retroceder y explorar otras ramas. 
Aquí los eventos se registran como `[reloj_vector, tipo, mensaje, emisor, receptor]`, donde los sets se convierten a tuplas ordenadas (para mantener la compatibilidad con las estructuras hashables de Python).
