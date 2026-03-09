from abstracciones.Problem import Problem
from abstracciones.Node import Node
from collections import deque
from typing import Optional


def depth_first_graph_search(problem: Problem) -> Optional[Node]:
    """
Realiza una búsqueda en profundidad sobre un grafo.

Este algoritmo explora primero el camino más profundo disponible
antes de retroceder. Para ello usa una estructura LIFO (pila),
de modo que el último nodo en entrar es el primero en salir.

A diferencia de la versión tree search, aquí se mantiene un conjunto
de estados explorados para evitar ciclos y no volver a expandir
estados ya visitados.

Args:
    problem:
        Problema de búsqueda que define el estado inicial, las acciones
        posibles, la transición entre estados y la prueba de meta.

Returns:
    El nodo meta si encuentra una solución; en caso contrario, None.
"""

    root = Node(state=problem.initial_state)

    # LIFO
    frontier = [root]  # Stack

    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        print("Explorando nodo: ", node.state)
        frontier.extend(child for child in node.expand(problem=problem)
                        if child.state not in explored and child not in frontier)
    return None
