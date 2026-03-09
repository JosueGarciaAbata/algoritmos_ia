
from collections import deque
from typing import Optional

from abstracciones.Problem import Problem
from abstracciones.Node import Node
  

def breadth_first_graph_search(problem: Problem) -> Optional[Node]:
    """
    Realiza una búsqueda en anchura sobre un grafo.

    Este algoritmo explora primero los nodos más cercanos a la raíz,
    es decir, recorre el problema por niveles.

    Usa:
    - una cola FIFO (`frontier`) para mantener el orden de expansión
    - un conjunto de visitados (`explored`) para no volver a expandir
      estados ya explorados

    Es una búsqueda sobre grafos, no sobre árboles, porque evita repetir
    estados ya visitados.

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

    # 3) Conjunto de estados visitados
    explored = set()

    # 4) Mientras haya nodos...
    while frontier:
        node = frontier.popleft()

        # 5) Revisamos meta
        if problem.goal_test(node.state):
            return node

        print("Expandiendo nodo con estado:", node.state)

        explored.add(node.state)

        # 6) Expandimos
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)

    return None