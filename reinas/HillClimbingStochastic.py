import random
from typing import List

from reinas.LocalNQueensProblem import LocalNQueensProblem
from reinas.Node import Node

def hill_climbing(problem: LocalNQueensProblem) -> Node:
    current = Node(state=problem.initial_state)

    while True:
        candidates: List[Node] = []
        weights: List[int] = []

        current_value = problem.value(current.state)

        for action in problem.actions(current.state):
            neighbor = current.child_node(problem, action)
            improvement = problem.value(neighbor.state) - current_value

            if improvement > 0:
                candidates.append(neighbor)
                weights.append(improvement)

        if not candidates:
            print("No se encontraron vecinos mejores. Terminando.")
            return current

        current = weighted_choice(candidates, weights)


def weighted_choice(candidates: List[Node], weights: List[int]) -> Node:
    return random.choices(candidates, weights=weights, k=1)[0]