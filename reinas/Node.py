from typing import Any, List, List
from abstracciones.Problem import Problem
from reinas.LocalNQueensProblem import LocalNQueensProblem

class Node:

  def __init__(self,
               state: Any) -> None:
    
    self.state = state

  def expand(self, problem: LocalNQueensProblem) -> List[Node]:
    # 1) Pedimos al problema las acciones validas desde el
    # estado actual.
    actions: List[Any] = problem.actions(self.state)

    # 2) Por cada accion valida, creamos un hijo.
    children: List[Node] = []
    for action in actions:
      child = self.child_node(problem, action)
      children.append(child)

    return children
  
  def child_node(self, problem: LocalNQueensProblem, action: Any) -> Node:
    # 1) Calculamos el estado siguiente usando el problema concreto.
    next_state: Any = problem.result(self.state, action)

    # 2) Creamos el nodo hijo.
    return Node(state=next_state)