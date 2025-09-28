"""Definición base de un nodo."""

import simpy


class Nodo:
    """Representa un nodo genérico.

    Atributos:
    - id_nodo: identificador entero del nodo.
    - vecinos: lista de vecinos.
    - canal_entrada: canal por el que el nodo recibe mensajes.
    - canal_salida: canal usado por el nodo para enviar mensajes.
    """

    def __init__(
        self,
        id_nodo: int,
        vecinos: list,
        canal_entrada: simpy.Store,
        canal_salida: simpy.Store,
    ):
        """Inicializa los atributos básicos del nodo.

        Args:
            id_nodo: identificador único del nodo.
            vecinos: lista de vecinos (IDs o referencias a objetos nodo).
            canal_entrada: canal para recibir mensajes.
            canal_salida: canal para enviar mensajes.
        """
        self._id_nodo = id_nodo
        self._vecinos = vecinos
        self._canal_entrada = canal_entrada
        self._canal_salida = canal_salida

    def get_id(self) -> int:
        """Devuelve el identificador del nodo."""
        return self._id_nodo

    def get_vecinos(self) -> list:
        """Regresa la lista de vecinos."""
        return self._vecinos

    def get_canal_entrada(self) -> simpy.Store:
        """Devuelve el canal de entrada (usado para recibir mensajes)."""
        return self._canal_entrada

    def get_canal_salida(self) -> simpy.Store:
        """Devuelve el canal de salida (usado para enviar mensajes)."""
        return self._canal_salida
