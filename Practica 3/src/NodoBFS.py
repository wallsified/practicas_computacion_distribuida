import simpy
from Nodo import *
from Canales.CanalRecorridos import *

TICK = 1

class NodoBFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo BFS. '''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo BFS. '''
        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)

        """Representa un nodo BFS.

        Atributos:
        - padre = por convención, en el PDF, especifíca que cada nodo sea su propio padre.
        - distancia = valor máximo permitido, nos indica que el nodo no ha sido visitado.
        - hijos = nodos de los cuales recibimos mensaje, es una lista.
        - expected_msg = cantidad de mensajes BACK a esperar.
        """
        self.padre = id_nodo
        self.distancia = float('inf')
        self.hijos = []
        self.expected_msg = 0

    def bfs(self, env):
        ''' Algoritmo BFS distribuido. '''

        ''' Algoritmo:
        1.	El nodo distinguido es el único que inicia el proceso. Se envía a sí mismo un mensaje GO con una distancia de -1.
        2.	Cuando un nodo recibe un mensaje GO por primera vez:
            2.1	Establece al emisor como su padre y fija su distancia como la distancia del emisor + 1.
            2.2	Establece su contador expected_msg al número total de vecinos que tiene, excluyendo a su nuevo padre.
            2.3	Envía un mensaje GO con su nueva distancia a todos esos vecinos.
        3.	Si un nodo recién visitado no tiene más vecinos a quienes mandar el mensaje (es decir, expected_msg es 0), 
        inmediatamente envía un mensaje BACK con la respuesta 'yes' a su padre.
        4.	Si un nodo que ya fue visitado (ya tiene un padre y una distancia) recibe otro mensaje GO, 
        simplemente lo rechaza enviando un BACK con la respuesta 'no' al emisor de ese mensaje.
        5.	Cuando un nodo recibe un mensaje BACK:
            5.1	Disminuye en uno su contador expected_msg.
            5.2	Si la respuesta en el mensaje es 'yes', añade al emisor a su lista de hijos.
        6.	Una vez que el contador expected_msg de un nodo llega a cero, significa que ha recibido respuesta de todas sus ramas. 
        En ese momento, envía un BACK con respuesta 'yes' a su propio padre para notificar que su sub-árbol está completo.
        7.	El algoritmo termina cuando el nodo distinguido también ha recibido todas las respuestas esperadas 
        y su contador expected_msg llega a cero.
        '''
        if self.distinguido:
            mensaje = ('GO', -1, self.id_nodo)
            self.canal_salida.envia(mensaje, [self.id_nodo])

        while True:
            mensaje = yield self.canal_entrada.get()
            tipo = mensaje[0]

            if tipo == 'GO':
                _, dist_emisor, id_emisor = mensaje
                
                if self.distancia == float('inf'):
                    self.padre = id_emisor
                    self.distancia = dist_emisor + 1
                    vecinos_a_enviar = [v for v in self.vecinos if v != self.padre]
                    self.expected_msg = len(vecinos_a_enviar)
                    
                    if self.expected_msg == 0:
                        msg_back = ('BACK', 'yes', self.distancia, self.id_nodo)
                        self.canal_salida.envia(msg_back, [self.padre])
                    else:
                        msg_go = ('GO', self.distancia, self.id_nodo)
                        self.canal_salida.envia(msg_go, vecinos_a_enviar)
                else:
                    msg_back = ('BACK', 'no', self.distancia, self.id_nodo)
                    self.canal_salida.envia(msg_back, [id_emisor])

            elif tipo == 'BACK':
                _, respuesta, _, id_hijo = mensaje
                
                if respuesta == 'yes':
                    self.hijos.append(id_hijo)
                
                self.expected_msg -= 1
                
                if self.expected_msg == 0:
                    if not self.distinguido:
                        msg_back = ('BACK', 'yes', self.distancia, self.id_nodo)
                        self.canal_salida.envia(msg_back, [self.padre])
                    else:
                        print(f"Nodo {self.id_nodo}: El árbol de expansión BFS ha sido construido.")