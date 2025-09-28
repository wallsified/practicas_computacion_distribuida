"""Nodo generador que implementa el algoritmo de construcción de árbol
usando flooding (GO/BACK).

El nodo distinguido (ID 0) inicia enviando mensajes "GO" a sus vecinos.
Cuando un nodo recibe "GO" por primera vez, fija al remitente como padre y
propaga "GO" al resto de sus vecinos. Cuando un nodo ha recibido respuestas
"BACK" de todos sus hijos potenciales, responde con un "BACK" hacia su
padre indicando si tiene hijos o no (valor distinto de None).
"""

import simpy

from Canales.CanalBroadcast import *
from Nodo import Nodo

TICK = 1


class NodoGenerador(Nodo):
    """
    Implementa la interfaz de Nodo para el algoritmo de generación del árbol.
    usando mensajes GO/BACK.

    Atributos propios del algoritmo:
    - padre: id o referencia al nodo padre (None si no conoce aún al padre).
    - hijos: lista de ids/referencias a los hijos descubiertos.
    - mensajes_esperados: contador de BACKs que espera recibir antes de
      responder al padre.
    """

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        """Inicializa el nodo generador.

        Args:
            id_nodo: identificador del nodo.
            vecinos: lista de vecinos (IDs o referencias).
            canal_entrada: `simpy.Store` para recibir mensajes.
            canal_salida: canal con método `envia(mensaje, destinos)`.
        """
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida

        # Atributos propios del algoritmo
        self.padre = (
            None if id_nodo != 0 else id_nodo
        )  # Si es el nodo distinguido, el padre es el mismo
        self.hijos = list()
        self.mensajes_esperados = len(vecinos)  # Cantidad de mensajes que esperamos

    def genera_arbol(self, env):
        if self.id_nodo == 0:
            self.padre = self.id_nodo
            self.mensajes_esperados = len(self.vecinos)
            for vecino in self.vecinos:
                self.canal_salida.envia(
                    {"tipo": "GO", "origen": self.id_nodo}, [vecino]
                )
        else:
            self.padre = None
        self.hijos = []

        while True:
            mensaje = yield self.canal_entrada.get()
            tipo = mensaje.get("tipo")
            origen = mensaje.get("origen")

            if tipo == "GO":
                # Si el nodo aún no tiene padre, el remitente se convierte en padre
                if self.padre is None:
                    self.padre = origen
                    # Esperamos mensajes de todos los vecinos excepto el padre
                    self.mensajes_esperados = len(self.vecinos) - 1
                    vecinos_sin_padre = [v for v in self.vecinos if v != origen]
                    if self.mensajes_esperados == 0:
                        # No hay otros vecinos: respondemos BACK inmediatamente
                        self.canal_salida.envia(
                            {
                                "tipo": "BACK",
                                "origen": self.id_nodo,
                                "valor": self.id_nodo,
                            },
                            [origen],
                        )
                    else:
                        # Propagamos GO al resto de vecinos
                        for vecino in vecinos_sin_padre:
                            self.canal_salida.envia(
                                {"tipo": "GO", "origen": self.id_nodo}, [vecino]
                            )
                else:
                    # Si ya tenemos padre, rechazamos la propuesta indicando
                    # que no formaremos parte de la sub-árbol (valor None)
                    self.canal_salida.envia(
                        {"tipo": "BACK", "origen": self.id_nodo, "valor": None},
                        [origen],
                    )

            elif tipo == "BACK":
                # Recibimos una respuesta de uno de nuestros hijos potenciales
                self.mensajes_esperados -= 1
                if mensaje.get("valor") is not None:
                    # El hijo informó que tiene/era parte del sub-árbol
                    self.hijos.append(origen)
                # Cuando recibimos todos los BACKs, respondemos al padre si
                # no somos el nodo raíz.
                if self.mensajes_esperados == 0:
                    if self.padre != self.id_nodo:
                        self.canal_salida.envia(
                            {
                                "tipo": "BACK",
                                "origen": self.id_nodo,
                                "valor": self.id_nodo,
                            },
                            [self._get_vecino_por_id(self.padre)],
                        )

    def _get_vecino_por_id(self, id_buscar):
        """Devuelve el vecino correspondiente al id buscado.

        Acepta que los elementos de `self.vecinos` sean:
        - enteros (IDs): en ese caso devuelve el entero si coincide.
        - objetos nodo: se intentan `get_id()` y el atributo `id_nodo`.

        Devuelve `None` si no encuentra correspondencia.
        """
        for vecino in self.vecinos:
            # Vecino es un ID (int)
            if isinstance(vecino, int):
                if vecino == id_buscar:
                    return vecino
                continue

            # Vecino es un objeto: intentamos varias maneras de obtener su id
            if hasattr(vecino, "get_id"):
                try:
                    if vecino.get_id() == id_buscar:
                        return vecino
                except Exception:
                    pass
            if hasattr(vecino, "id_nodo"):
                try:
                    if vecino.id_nodo == id_buscar:
                        return vecino
                except Exception:
                    pass

        return None
