from abstracciones.Problem import Problem
from typing import List, Optional, Any

class Node:

  def __init__(self,
               state: Any,
               parent: Optional[Node] = None,
               action: Optional[Any] = None,
               path_cost: float = 0.0) -> None:
    self.state: Any = state
    self.parent: Optional[Node] = parent
    self.action: Optional[Any] = action
    self.path_cost: float = path_cost
    self.depth = 0 if parent is None else parent.depth + 1

  # Generacion de lo sucesores (nuevos nodos)

  def expand(self, problem: Problem) -> List[Node]:
    """
    Genera los nodos hijos (sucesores) a partir de este nodo.
    """

    # 1) Pedimos al problema las acciones validas desde el
    # estado actual.

    actions: List[Any] = problem.actions(self.state)

    # 2) Por cada accion valida, creamos un hijo.
    children: List[Node] = []
    for action in actions:
      child = self.child_node(problem, action)
      children.append(child)

    return children
  
  def child_node(self, problem: Problem, action: Any) -> Node:
    """
    Crea un unico nodo hijo aplicando 'action'.
    """

    # 1) Calculamos el estado siguiente usando el problema concreto.
    next_state: Any = problem.result(self.state, action)

    # 2) Como no estamos usando path_cost del problema,
    # asumimos costo uniforme de 1 por movimiento.
    next_cost: float = problem.path_cost(self.path_cost, self.state, action, next_state)

    # 3) Creamos el nodo hijo.
    return Node(
      state=next_state,
      parent=self,
      action=action,
      path_cost=next_cost
    )

  def solution(self) -> List[Any]:
    """
    Devuelve la secuencia de acciones para llegar a este nodo desde la raiz.
    """

    return [node.action for node in self.path() if node.action is not None]

  # Reconstruccion de camino
  def path(self) -> List[Node]:
    """
    Devuelve la secuencia de nodos desde el nodo raiz hasta este nodo.
    """

    node: Optional[Node] = self
    nodes: List[Node] = []

    # Subimos por la cadena de padres.
    while node is not None:
      nodes.append(node)
      node = node.parent

    # Invertimos la lista para que vaya de raiz a este nodo.
    nodes.reverse()
    return nodes
  
  def __eq__(self, other):
    return isinstance(other, Node) and self.state == other.state

  def __hash__(self):
    return hash(self.state)