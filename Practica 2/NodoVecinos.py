"""Nodo que descubre los vecinos de sus vecinos.

Este nodo envía la lista de sus vecinos a cada vecino y luego recoge las
respuestas (listas) para construir el conjunto `identifiers` con los
identificadores de segundo nivel.
"""

import simpy

from Canales.CanalBroadcast import *
from Nodo import Nodo


class NodoVecinos(Nodo):
    """
    Implementa la interfaz de Nodo para el algoritmo de descubrimiento de vecinos.

    Comportamiento:
    - Envía su lista de vecinos a cada vecino.
    - Espera recibir, por `canal_entrada`, listas con los vecinos de cada
      vecino y acumula todos los identificadores en `identifiers`.
    """

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        """Inicializa el nodo.

        Args:
            id_nodo: identificador del nodo.
            vecinos: iterables de vecinos (IDs o referencias).
            canal_entrada: canal para recibir mensajes.
            canal_salida: canal para enviar mensajes.
            identifiers: conjunto donde se guardan los identificadores de los vecinos de los vecinos.
        """
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.identifiers = set()

    def conoceVecinos(self, env):
        """
        Algoritmo que hace que el nodo conozca a los vecinos de sus vecinos.
        Lo guarda en la variable identifiers.
        """

        # Envíamos la lista de nuestros vecinos a nuestros vecinos.
        self.canal_salida.envia(self.vecinos, self.vecinos)
        # Y esperamos los mensajes de nuestros vecinos.
        while True:
            mensaje = yield self.canal_entrada.get()
            self.identifiers.update(mensaje)
