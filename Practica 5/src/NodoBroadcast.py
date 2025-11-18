import simpy
from Nodo import *
from Canales.CanalRecorridos import *
from random import randint, uniform


class NodoBroadcast(Nodo):
    def __init__(
        self,
        id_nodo: int,
        vecinos: list,
        canal_entrada: simpy.Store,
        canal_salida: simpy.Store,
    ):
        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)
        self.mensaje = None
        self.reloj = 0
        self.eventos = []
        self.padres = set()  # Para evitar enviar de vuelta al padre

    def broadcast(self, env: simpy.Environment, data="Mensaje"):
        """
        Algoritmo de Broadcast con reloj de Lamport.
        El sistema es parcialmente asíncrono con delays aleatorios.
        """
        # Delay aleatorio inicial para asincronía
        yield env.timeout(uniform(0.1, 0.5))

        if self.distinguido:
            # El nodo distinguido inicia el broadcast
            self.mensaje = data

            # Enviar mensaje a todos los vecinos
            for vecino in self.vecinos:
                # Incrementar reloj antes de cada envío
                self.reloj += 1

                # Registrar evento de envío antes de enviar
                self.eventos.append([self.reloj, "E", data, self.id_nodo, vecino])

                # Delay aleatorio antes de cada envío
                yield env.timeout(uniform(0.1, 0.3))

                # Enviar mensaje con el reloj
                mensaje = (data, self.reloj, self.id_nodo)
                yield self.canal_salida.envia(mensaje, [vecino])

        # Todos los nodos (incluyendo el distinguido) procesan mensajes recibidos
        while True:
            # Esperar a recibir un mensaje
            try:
                # Delay aleatorio antes de recepción
                yield env.timeout(uniform(0.1, 0.3))

                mensaje = yield self.canal_entrada.get()
                data_recibido, reloj_recibido, id_emisor = mensaje

                # Actualizar reloj de Lamport: max(reloj_local, reloj_recibido) + 1
                self.reloj = max(self.reloj, reloj_recibido) + 1

                # Registrar evento de recepción
                self.eventos.append(
                    [self.reloj, "R", data_recibido, id_emisor, self.id_nodo]
                )

                # Si es la primera vez que recibimos el mensaje
                if self.mensaje is None:
                    self.mensaje = data_recibido
                    self.padres.add(id_emisor)

                    # Reenviar a todos los vecinos excepto al padre
                    for vecino in self.vecinos:
                        if vecino != id_emisor:
                            # Incrementar reloj antes de enviar
                            self.reloj += 1

                            # Registrar evento de envío
                            self.eventos.append(
                                [self.reloj, "E", data_recibido, self.id_nodo, vecino]
                            )

                            # Delay aleatorio antes de cada envío
                            yield env.timeout(uniform(0.1, 0.3))

                            # Enviar mensaje con el reloj
                            mensaje_reenvio = (data_recibido, self.reloj, self.id_nodo)
                            yield self.canal_salida.envia(mensaje_reenvio, [vecino])
                else:
                    # Ya teníamos el mensaje, solo agregar al padre si no estaba
                    self.padres.add(id_emisor)

            except simpy.Interrupt:
                break
