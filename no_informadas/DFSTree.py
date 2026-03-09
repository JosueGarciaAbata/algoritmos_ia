from abstracciones.Problem import Problem
from abstracciones.Node import Node
from collections import deque
from typing import Optional

def depth_first_tree_search(problem: Problem) -> Optional[Node]:
    """
Realiza una búsqueda en profundidad sobre un árbol.

Este algoritmo explora primero el camino más profundo disponible
antes de retroceder. Para ello usa una estructura LIFO (pila),
de modo que el último nodo en entrar es el primero en salir.

A diferencia de la versión graph search, aquí no se mantiene un
conjunto de visitados. Por eso, si el problema tiene ciclos o
estados repetidos, el algoritmo puede volver a generarlos.

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

    # 2) Cola LIFO (stack)
    frontier = [root]

    # 3) Mientras haya nodos...
    while frontier:
        node = frontier.pop()

        # 4) Revisamos meta
        if problem.goal_test(node.state):
            return node

        print("Expandiendo nodo con estado:", node.state)

        # 5) Expandimos
        frontier.extend(node.expand(problem=problem))

    return None