from collections import deque
from typing import Any, Deque, Dict, Optional, Tuple

from abstracciones.Problem import Problem
from abstracciones.Node import Node


def bidirectional_breadth_first_graph_search(problem: Problem) -> Optional[Node]:
    """
    Realiza una búsqueda bidireccional en anchura sobre un grafo.

    En lugar de buscar solo desde el estado inicial, este algoritmo
    avanza al mismo tiempo desde:
    - el estado inicial
    - el estado meta

    La búsqueda termina cuando ambas exploraciones se encuentran en
    un mismo estado. Luego, se combinan ambos caminos para reconstruir
    una solución completa.

    Este enfoque puede reducir la cantidad de nodos explorados en
    comparación con una BFS tradicional, especialmente cuando el
    espacio de búsqueda es grande.

    Args:
        problem:
            Problema de búsqueda que define el estado inicial, el estado
            meta, las acciones posibles y la transición entre estados.

    Returns:
        Un nodo final que representa el camino completo desde el inicio
        hasta la meta, o None si no encuentra solución.
    """

    if problem.initial_state == problem.goal_state:
        return Node(problem.initial_state)

    start_node = Node(problem.initial_state)
    goal_node = Node(problem.goal_state)

    frontier_start: Deque[Node] = deque([start_node])
    frontier_goal: Deque[Node] = deque([goal_node])

    visited_start: Dict[Any, Node] = {start_node.state: start_node}
    visited_goal: Dict[Any, Node] = {goal_node.state: goal_node}

    while frontier_start and frontier_goal:
        # Expandimos primero la frontera más pequeña.
        if len(frontier_start) <= len(frontier_goal):
            meeting = _expand_one_level(problem, frontier_start, visited_start, visited_goal)
            if meeting is not None:
                meeting_from_start, meeting_from_goal = meeting
                return _merge_paths(problem, meeting_from_start, meeting_from_goal)
        else:
            meeting = _expand_one_level(problem, frontier_goal, visited_goal, visited_start)
            if meeting is not None:
                meeting_from_goal, meeting_from_start = meeting
                return _merge_paths(problem, meeting_from_start, meeting_from_goal)

    return None


def _expand_one_level(
    problem: Problem,
    frontier: Deque[Node],
    own_visited: Dict[Any, Node],
    other_visited: Dict[Any, Node]
) -> Optional[Tuple[Node, Node]]:
    """
    Expande exactamente un nivel BFS de una frontera.

    Retorna:
        (node_from_this_side, node_from_other_side)
    si encuentra un estado ya visitado por la búsqueda opuesta.
    """

    level_size = len(frontier)

    for _ in range(level_size):
        current = frontier.popleft()

        for child in current.expand(problem):
            if child.state in own_visited:
                continue

            own_visited[child.state] = child

            if child.state in other_visited:
                return child, other_visited[child.state]

            frontier.append(child)

    return None


def _merge_paths(problem: Problem, meeting_from_start: Node, meeting_from_goal: Node) -> Node:
    """
    Une:
        initial -> ... -> meeting
    con:
        goal -> ... -> meeting

    y construye un único Node final compatible con path() y solution().
    """

    # Camino normal desde el inicio hasta el punto de encuentro.
    forward_path = meeting_from_start.path()  # [start, ..., meeting]

    # Camino desde la meta hasta el punto de encuentro.
    backward_path = meeting_from_goal.path()  # [goal, ..., meeting]

    # Lo invertimos para obtener:
    # [meeting, ..., goal]
    backward_path.reverse()

    # Reutilizamos el nodo de encuentro del lado forward.
    current = forward_path[-1]

    # Saltamos el primer nodo para no duplicar el meeting node.
    for node in backward_path[1:]:
        current = Node(
            state=node.state,
            parent=current,
            action=node.action,
            path_cost=current.path_cost + 1
        )

    return current