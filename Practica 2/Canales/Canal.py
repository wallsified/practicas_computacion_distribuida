"""
Archivo de la interfaz del canal.
"""

import simpy


class Canal:
    """
    Interfaz que modela el comportamiento que cualquier canal debe tomar.
    """

    def __init__(self, env: simpy.Environment, capacidad):
        """Inicializa el canal."""
        raise NotImplementedError("Este método debe ser implementado por la subclase.")

    def envia(self, mensaje, vecinos):
        """Envia un mensaje a los canales de entrada de los vecinos."""
        raise NotImplementedError("Este método debe ser implementado por la subclase.")

    def crea_canal_de_entrada(self):
        """Creamos un objeto Store en el que un nodo recibirá los mensajes."""
        raise NotImplementedError("Este método debe ser implementado por la subclase.")
