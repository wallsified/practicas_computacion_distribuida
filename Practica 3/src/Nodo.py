import simpy


class Nodo:
    """Representa un nodo.

    Cada nodo tiene un id, una lista de vecinos y dos canales de comunicación.
    Los métodos que tiene son únicamente getters para la información básica.
    """

    def __init__(
        self,
        id_nodo: int,
        vecinos: list,
        canal_entrada: simpy.Store,
        canal_salida: simpy.Store,
    ):
        """Inicializa los atributos del nodo."""

        """Representa un nodo genérico.

        Atributos:
        - id_nodo: identificador entero del nodo.
        - vecinos: lista de vecinos.
        - canal_entrada: canal por el que el nodo recibe mensajes.
        - canal_salida: canal usado por el nodo para enviar mensajes.
        - distinguido: nodo de partida, es con el que se inician los algoritmos.
        """
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.distinguido = id_nodo == 0

    def get_id(self) -> int:
        """Regresa el id del nodo."""
        return self.id_nodo
