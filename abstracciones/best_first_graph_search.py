from abstracciones.Problem import Problem
from abstracciones.Node import Node

import heapq
from itertools import count
from typing import Any, Callable, Iterable

def best_first_graph_search(problem: Problem, f: Callable[[Node], float], display=False):
    """
    Realiza una búsqueda 'primero el mejor' sobre un grafo.

    La idea del algoritmo es siempre expandir primero el nodo que tenga
    el menor valor según la función `f(node)`.

    La función `f` define qué significa "mejor":
    - Si `f(node)` es una heurística, obtenemos una búsqueda voraz (greedy).
    - Si `f(node)` es el costo acumulado, obtenemos costo uniforme.
    - Si `f(node)` combina costo + heurística, obtenemos A*.

    Parámetros:
        problem:
            El problema de búsqueda que define el estado inicial,
            las acciones, la prueba de meta y la transición entre estados.

        f:
            Función de evaluación que asigna una prioridad a cada nodo.
            El algoritmo expande primero el nodo con menor valor de `f`.

        display:
            Si es True, imprime información básica al encontrar la solución.

    Retorna:
        El nodo meta si encuentra una solución; en caso contrario, None.

    Nota:
        Esta es una búsqueda sobre grafos, no sobre árboles.
        Por eso usa:
        - `frontier`: nodos pendientes por explorar
        - `explored`: estados ya expandidos
    """

    # 1) Crear el nodo inicial a partir del estado inicial del problema.
    node = Node(problem.initial_state)

    # 2) Crear la frontera como una cola de prioridad mínima.
    #    El nodo con menor f(node) saldrá primero.
    frontier = PriorityQueue('min', f)
    frontier.append(node)

    # 3) Conjunto de estados ya explorados.
    explored = set()

    # 4) Repetir mientras haya nodos pendientes en la frontera.
    while frontier:
        # Sacar el nodo con mejor prioridad.
        node = frontier.pop()

        # 5) Si el nodo actual ya es meta, devolverlo.
        if problem.goal_test(node.state):
            if display:
                print(
                    len(explored),
                    "paths have been expanded and",
                    len(frontier),
                    "paths remain in the frontier"
                )
            return node

        # 6) Marcar el estado actual como explorado.
        explored.add(tuple(map(tuple, node.state)))

        # 7) Expandir el nodo actual para generar sus hijos.
        for child in node.expand(problem):

            # Si el hijo no fue explorado y tampoco está en la frontera,
            # se agrega como nuevo candidato.
            if tuple(map(tuple, child.state)) not in explored and child not in frontier:
                frontier.append(child)

            # Si el hijo ya está en la frontera, se compara su prioridad.
            # Si el nuevo camino es mejor, se reemplaza el anterior.
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)

    # 8) Si la frontera se vacía, no se encontró solución.
    return None


class PriorityQueue:
    """
    Cola de prioridad basada en heap.

    - Si order='min', sale primero el elemento con menor f(x).
    - Si order='max', sale primero el elemento con mayor f(x).

    La cola también permite:
    - revisar si un elemento ya está dentro: `item in frontier`
    - consultar su prioridad actual: `frontier[item]`
    - eliminarlo: `del frontier[item]`
    """

    def __init__(self, order: str = "min", f: Callable[[Any], float] = lambda x: x) -> None:
        """
        Crea una cola de prioridad.

        Args:
            order:
                'min' para que salga primero el menor valor de f(x),
                'max' para que salga primero el mayor valor de f(x).

            f:
                Función que calcula la prioridad de cada elemento.
        """
        if order not in ("min", "max"):
            raise ValueError("order must be either 'min' or 'max'")

        self.heap: list[tuple[float, int, Any]] = []
        self._counter = count()

        if order == "min":
            self.f = f
        else:
            # Convertimos el problema de máximo a mínimo usando el negativo.
            self.f = lambda item: -f(item)

    def append(self, item: Any) -> None:
        """
        Inserta un elemento en la cola con su prioridad correspondiente.
        """
        priority = self.f(item)
        # El contador evita errores cuando dos elementos tienen la misma prioridad.
        heapq.heappush(self.heap, (priority, next(self._counter), item))

    def extend(self, items: Iterable[Any]) -> None:
        """
        Inserta varios elementos en la cola.
        """
        for item in items:
            self.append(item)

    def pop(self) -> Any:
        """
        Extrae y devuelve el elemento con mejor prioridad.

        Returns:
            El item con menor prioridad si order='min',
            o con mayor prioridad si order='max'.

        Raises:
            Exception: si la cola está vacía.
        """
        if not self.heap:
            raise Exception("Trying to pop from empty PriorityQueue.")

        _, _, item = heapq.heappop(self.heap)
        return item

    def __len__(self) -> int:
        """
        Devuelve la cantidad actual de elementos en la cola.
        """
        return len(self.heap)

    def __contains__(self, key: Any) -> bool:
        """
        Devuelve True si `key` ya está en la cola.
        """
        return any(item == key for _, _, item in self.heap)

    def __getitem__(self, key: Any) -> float:
        """
        Devuelve la prioridad asociada a `key`.

        Esto permite hacer cosas como:
            frontier[node]

        Raises:
            KeyError: si el elemento no está en la cola.
        """
        for priority, _, item in self.heap:
            if item == key:
                return priority
        raise KeyError(f"{key} is not in the priority queue")

    def __delitem__(self, key: Any) -> None:
        """
        Elimina la primera ocurrencia de `key` dentro de la cola.

        Esto es útil cuando encuentras una mejor versión de un nodo
        y quieres reemplazar la versión anterior.

        Raises:
            KeyError: si el elemento no está en la cola.
        """
        for index, (_, _, item) in enumerate(self.heap):
            if item == key:
                del self.heap[index]
                heapq.heapify(self.heap)
                return

        raise KeyError(f"{key} is not in the priority queue")