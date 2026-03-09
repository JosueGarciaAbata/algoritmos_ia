from __future__ import annotations

from collections import deque
from typing import Optional

from NodeParaOvejaProblema import Node
from LoboConOvejaProblema import LoboOvejaColProblem


def breadth_first_tree_search(problem: LoboOvejaColProblem) -> Optional[Node]:
    """
    BFS Tree Search (sin visitados).

    Retorna:
        Un Node meta (si lo encuentra) o None.
    """

    # 1) Creamos el nodo raíz correctamente:
    #    - problem: referencia al problema
    #    - state: estado inicial
    root = Node(problem=problem, state=problem.initial)

    # 2) Cola FIFO (BFS)
    frontier = deque([root])

    # 3) Mientras haya nodos...
    while frontier:
        node = frontier.popleft()

        # 4) Revisamos meta
        if problem.goal_test(node.state):
            return node

        # 5) Expandimos
        frontier.extend(node.expand())

    return None