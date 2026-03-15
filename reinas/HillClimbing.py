from reinas.LocalNQueensProblem import LocalNQueensProblem
from reinas.Node import Node

def hill_climbing(problem: LocalNQueensProblem) -> Node:

  current = Node(state=problem.initial_state)
  while True:
    best_neighbor = current

    for action in problem.actions(current.state):
      neighbor = current.child_node(problem, action)

      # Si el vecino es mejor que el mejor vecino encontrado hasta ahora, lo guardamos.
      if problem.conflicts(neighbor.state) < problem.conflicts(best_neighbor.state):
        best_neighbor = neighbor

    # Solo conviene avanzar si el vecino es mejor que el estado actual.
    if problem.conflicts(best_neighbor.state) >= problem.conflicts(current.state):
      return current

    current = best_neighbor