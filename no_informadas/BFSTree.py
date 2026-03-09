from abstracciones.Problem import Problem
from abstracciones.Node import Node
from collections import deque
from typing import Optional

def breadth_first_tree_search(problem: Problem) -> Optional[Node]:
    """
Realiza una búsqueda en anchura sobre un árbol.

Este algoritmo explora primero los nodos más cercanos a la raíz,
es decir, avanza por niveles usando una cola FIFO.

A diferencia de la versión graph search, aquí no se lleva un conjunto
de visitados. Por eso, el algoritmo puede volver a generar estados
repetidos si el problema lo permite.

Args:
    problem:
        Problema de búsqueda que define el estado inicial, las acciones
        posibles, la transición entre estados y la prueba de meta.

Returns:
    El nodo meta si encuentra una solución; en caso contrario, None.
"""

    # 1) Creamos el nodo raíz correctamente:
    #    - problem: referencia al problema
    #    - state: estado inicial
    root = Node(state=problem.initial_state)

    # 2) Cola FIFO (BFS)
    frontier = deque([root])

    # 3) Mientras haya nodos...
    while frontier:
        node = frontier.popleft()

        # 4) Revisamos meta
        if problem.goal_test(node.state):
            return node

        print("Expandiendo nodo con estado:", node.state)

        # 5) Expandimos
        frontier.extend(node.expand(problem=problem))

    return None