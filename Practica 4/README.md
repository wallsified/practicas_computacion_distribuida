# Práctica 4: Consenso

| Alumno                        | No. Cuenta |
|-------------------------------|------------|
| Paredes Zamudio Luis Daniel   | 318159926  |
| Reyna Mendez Cristian Ignacio | 320149579  |
| Lopez Ramirez Juan Carlos     | 316186021  |

## Resumen de la implementación de `NodoConsenso`

`NodoConsenso` extiende `Nodo` para implementar un algoritmo de consenso distribuido sin terminación temprana. Funciona de la siguiente manera:

- Cada nodo propone inicialmente su propio identificador como valor y, durante varias rondas, intercambia mensajes con sus vecinos para compartir y actualizar los valores propuestos. 
- En cada ronda, el nodo selecciona el valor mínimo recibido como su nuevo valor propuesto. Algunos nodos pueden estar configurados para fallar y dejar de participar en el protocolo. 
- Al finalizar las rondas, cada nodo elige como líder el primer valor válido recibido. 

Este proceso garantiza que todos los nodos correctos lleguen a un acuerdo sobre el líder, incluso en presencia de fallos.
