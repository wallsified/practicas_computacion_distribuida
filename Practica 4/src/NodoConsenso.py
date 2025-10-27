import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1


class NodoConsenso(Nodo):
    """Implementa la interfaz de Nodo para el algoritmo de Consenso."""

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        """Constructor de nodo que implemente el algoritmo de consenso."""
        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)
        # Atributos extra
        self.V = [None] * (len(vecinos) + 1)  # Llenamos la lista de Nodos
        self.V[id_nodo] = id_nodo
        self.New = set([id_nodo])
        self.rec_from = [None] * (len(vecinos) + 1)
        self.fallare = False  # Colocaremos esta en True si el nodo fallará
        self.lider = None  # La elección del lider.

    def consenso(self, env, f):
        """
        Algoritmo de consenso distribuido sin terminación temprana.
        Cada nodo ejecuta este proceso en paralelo.
        """
        # Determinar los nodos que fallarán
        nodos_fallaran = set(range(f))
        if self.id_nodo in nodos_fallaran:
            self.fallare = True

        ronda = 0
        valor = self.id_nodo  # Valor inicial propuesto por el nodo
        valores_recibidos = set([valor])

        # Número de rondas: f + 1 (según teoría de consenso sin terminación temprana)
        rondas_totales = f + 1

        while ronda < rondas_totales:
            # Si el nodo va a fallar, deja de enviar y procesar mensajes
            if self.fallare and ronda >= f:
                break

            # Enviar el valor actual a todos los vecinos
            yield self.canal_salida.envia((self.id_nodo, valor, ronda), self.vecinos)

            # Esperar a recibir mensajes de esta ronda
            mensajes_ronda = []
            tiempo_espera = TICK
            tiempo_final = env.now + tiempo_espera
            while env.now < tiempo_final:
                if len(self.canal_entrada.items) > 0:
                    mensaje = yield self.canal_entrada.get()
                    id_remitente, valor_remitente, ronda_mensaje = mensaje
                    if ronda_mensaje == ronda:
                        mensajes_ronda.append(valor_remitente)
                        self.V[id_remitente] = (
                            id_remitente  # Actualiza V con el remitente
                        )
                yield env.timeout(0.01)

            # Actualizar el conjunto de valores recibidos
            valores_recibidos.update(mensajes_ronda)

            # Para la siguiente ronda, el valor propuesto es el mínimo recibido
            valor = min(valores_recibidos)
            ronda += 1

        # Al finalizar, elegir el líder como el primer elemento no nulo de V
        self.lider = next(item for item in self.V if item is not None)
