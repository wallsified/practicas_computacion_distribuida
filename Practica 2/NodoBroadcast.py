"""
Implementación del algoritmo de Broadcast.
"""

import time

import simpy

from Canales.CanalBroadcast import *
from Nodo import Nodo

# La unidad de tiempo
TICK = 1


class NodoBroadcast(Nodo):
    """Implementa la interfaz de Nodo para el algoritmo de Broadcast."""

    def __init__(
        self, id_nodo, vecinos, canal_entrada, canal_salida, mensaje=None, grafica=None
    ):
        """
        Inicializa el nodo.

        Args:
            id_nodo: identificador del nodo (int).
            vecinos: colección de vecinos (IDs o referencias a objetos nodo).
            canal_entrada: canal para recibir mensajes.
            canal_salida: canal para enviar mensajes.
            mensaje: payload que el nodo 0 propaga al iniciar
            grafica: lista o colección de nodos para mapear IDs a nodos.
        """

        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.mensaje = mensaje
        if grafica is not None:
            self.canal_salida.set_grafica(grafica)

    def broadcast(self, env: simpy.Environment):
        """Proceso de simpy que propaga el mensaje por flooding.

        Comportamiento:
        - Si `id_nodo == 0`, envía el mensaje `self.mensaje` como `GO` a todos
          sus vecinos al iniciar.
        - En bucle, espera mensajes desde `canal_entrada`. Si recibe un mensaje
          con `tipo == 'GO'`, extrae `data` y lo reenvía a todos sus vecinos.
        """

        if self.id_nodo == 0:
            data = self.mensaje
            for vecino in self.vecinos:
                self.canal_salida.envia({"tipo": "GO", "data": data}, [vecino])
        else:
            data = None

        while True:
            mensaje = yield self.canal_entrada.get()
            if mensaje.get("tipo") == "GO":
                data = mensaje.get("data")
                for vecino in self.vecinos:
                    self.canal_salida.envia({"tipo": "GO", "data": data}, [vecino])
