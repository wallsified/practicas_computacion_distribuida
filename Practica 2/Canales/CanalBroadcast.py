import simpy
from Canales.Canal import Canal


class CanalBroadcast(Canal):
    """
    Clase que modela un canal, permite enviar mensajes one-to-many.
    Ahora acepta IDs de vecinos y busca el objeto nodo en la gráfica.
    """

    def __init__(self, env, grafica=None, capacidad=simpy.core.Infinity):
        """
        Inicializa el canal de broadcast.

        Args:
            env: entorno de simulación de simpy.
            grafica: lista o colección de nodos para mapear IDs a nodos.
            capacidad: capacidad del canal.
            grafica: lista o colección de nodos para mapear IDs a nodos.
        """
        self.env = env
        self.capacidad = capacidad
        self.canales = []
        self.grafica = grafica if grafica is not None else []

    def set_grafica(self, grafica):
        self.grafica = grafica

    def register_nodo(self, id_nodo, nodo):
        """Registrar dinámicamente un nodo en la grafica interna del canal.

        Esto permite que los nodos se registren al crearse sin depender de
        que el test asigne la grafica manualmente.

        Args:
            id_nodo: identificador del nodo.
            nodo: objeto nodo a registrar.
        """
        # Aseguramos que grafica sea una lista lo bastante larga
        if not isinstance(self.grafica, list):
            self.grafica = []
        if id_nodo >= len(self.grafica):
            # Extendemos con None hasta alcanzar el índice
            self.grafica.extend([None] * (id_nodo + 1 - len(self.grafica)))
        self.grafica[id_nodo] = nodo

    def _get_nodo_por_id(self, id_nodo):
        """Busca y devuelve el nodo con el ID dado en la grafica.
        Regresa None si no se encuentra.
        """
        # Si grafica es una lista indexable por id, intentamos acceso directo
        try:
            if isinstance(self.grafica, list) and 0 <= id_nodo < len(self.grafica):
                nodo = self.grafica[id_nodo]
                if nodo is not None:
                    return nodo
        except Exception:
            pass
        # Si no, hacemos la búsqueda tradicional
        for nodo in self.grafica or []:
            if nodo is None:
                continue
            if hasattr(nodo, "id_nodo") and nodo.id_nodo == id_nodo:
                return nodo
            if hasattr(nodo, "get_id") and nodo.get_id() == id_nodo:
                return nodo
        return None

    def envia(self, mensaje, vecinos):
        """
        Envia un mensaje a los canales de entrada de los vecinos.
        Ahora vecinos es una lista de IDs.
        """
        for vecino in vecinos:
            # Si el vecino es un entero (ID), intentamos mapearlo.
            if isinstance(vecino, int):
                # Si tenemos la grafica, obtenemos el nodo por id
                nodo = self._get_nodo_por_id(vecino) if self.grafica else None
                if nodo is not None:
                    canal_entrada = nodo.get_canal_entrada()
                    canal_entrada.put(mensaje)
                else:
                    # Si no tenemos la grafica, pero se han creado canales de entrada
                    # en el mismo orden que los nodos, usamos self.canales[id]
                    if 0 <= vecino < len(self.canales):
                        canal_entrada = self.canales[vecino]
                        canal_entrada.put(mensaje)
            else:
                # Si el vecino es un objeto nodo, usamos su canal de entrada
                try:
                    canal_entrada = vecino.get_canal_entrada()
                    canal_entrada.put(mensaje)
                except Exception:
                    # Silenciosamente ignoramos vecinos inválidos
                    continue

    def crea_canal_de_entrada(self):
        """
        Creamos un canal de entrada
        """
        canal_entrada = simpy.Store(self.env, capacity=self.capacidad)
        self.canales.append(canal_entrada)
        return canal_entrada
