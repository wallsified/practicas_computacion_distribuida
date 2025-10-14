import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoDFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo DFS. '''
        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)

        """Representa un nodo DFS.

        Atributos:
        - padre = por convención, en el PDF, especifíca que cada nodo sea su propio padre.
        - hijos = vecinos por los cuales realizamos la exploración.
        - visitados = nodos que ya fueron visitados/explorados.
        """
        self.padre = self.id_nodo
        self.hijos = []
        self.visitados = set()

    def dfs(self, env):
        ''' Algoritmo DFS. '''

        ''' Algoritmo:
    1.	El nodo distinguido inicia el recorrido. Se añade a sí mismo a su conjunto de visitados y 
    envía mensaje GO al vecino que tenga el menor ID.
    2.	Cuando un nodo recibe el GO:
        2.1	Establece al emisor como su padre y se añade a sí mismo al conjunto de visitados que venía en el mensaje.
        2.2	Revisa su lista de vecinos para encontrar a los que aún no han sido visitados.
        2.3	Si encuentra vecinos no visitados, elige al que tenga el menor ID, le envía el GO y continúa el recorrido.
    3.	Si un nodo recibe el GO pero se da cuenta de que todos sus vecinos ya están en el conjunto de visitados, no puede avanzar más.
    4.	Para retroceder, el nodo envía el BACK a su padre. Este mensaje también lleva el conjunto de visitados actualizado.
    5.	Actualiza su propio conjunto de visitados con el que viene en el mensaje.
    6.	Vuelve a revisar su lista de vecinos. Si encuentra uno que aún no ha sido visitado, 
    inicia una nueva exploración en profundidad por esa rama, eligiendo de nuevo al del menor ID y enviándole un GO.
    7.	Si un nodo recibe un BACK y se da cuenta de que ya no le quedan más vecinos por explorar, 
    continúa el proceso de retroceso enviando el BACK a su propio padre.
    8.	El algoritmo termina cuando el BACK regresa al nodo distinguido y este ya no tiene ningún vecino no visitado.
        '''
        
        if self.distinguido:
            self.padre = self.id_nodo
            self.visitados.add(self.id_nodo)
            
            if self.vecinos: 
                vecino_elegido = min(self.vecinos)
                mensaje = ('GO', self.visitados, self.id_nodo)
                self.canal_salida.envia(mensaje, [vecino_elegido])
                self.hijos.append(vecino_elegido)
        
        while True:
            mensaje = yield self.canal_entrada.get()
            tipo, visitados_msg, id_emisor = mensaje

            if tipo == 'GO':
                self.padre = id_emisor
                self.visitados = visitados_msg.union({self.id_nodo})
                vecinos_no_visitados = [v for v in self.vecinos if v not in self.visitados]
                
                if not vecinos_no_visitados:
                    msg_back = ('BACK', self.visitados, self.id_nodo)
                    self.canal_salida.envia(msg_back, [self.padre])
                    self.hijos = [] 
                else:
                    vecino_elegido = min(vecinos_no_visitados)
                    msg_go = ('GO', self.visitados, self.id_nodo)
                    self.canal_salida.envia(msg_go, [vecino_elegido])
                    self.hijos = [vecino_elegido]

            elif tipo == 'BACK':
                self.visitados = visitados_msg
                vecinos_no_visitados = [v for v in self.vecinos if v not in self.visitados]
                
                if not vecinos_no_visitados:
                    if self.distinguido:
                        print(f"Nodo {self.id_nodo}: El recorrido DFS ha finalizado.")
                    else:
                        msg_back = ('BACK', self.visitados, self.id_nodo)
                        self.canal_salida.envia(msg_back, [self.padre])
                else:
                    vecino_elegido = min(vecinos_no_visitados)
                    msg_go = ('GO', self.visitados, self.id_nodo)
                    self.canal_salida.envia(msg_go, [vecino_elegido])
                    self.hijos.append(vecino_elegido)