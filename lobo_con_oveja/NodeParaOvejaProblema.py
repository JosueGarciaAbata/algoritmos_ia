from __future__ import annotations  # Para usar 'Node' en anotaciones dentro de la clase
from typing import Any, List, Optional

from LoboConOvejaProblema import (
    LoboOvejaColProblem,
    State,
    Action
)


class Node:
    """
    Node = un nodo de búsqueda completamente acoplado
    a una instancia concreta de LoboOvejaColProblem.

    A diferencia de la versión abstracta:
    - NO recibe 'problem' como parámetro en expand().
    - Guarda una referencia directa al problema.
    - Asume costo uniforme (+1 por paso).

    Esto elimina la abstracción y hace el flujo más explícito.
    """

    def __init__(
        self,
        problem: LoboOvejaColProblem,
        state: State,
        parent: Optional[Node] = None,
        action: Optional[Action] = None,
        path_cost: float = 0.0,
    ):
        # 1) Guardamos referencia directa al problema.
        #    Ahora el nodo está acoplado a LoboOvejaColProblem.
        self.problem: LoboOvejaColProblem = problem

        # 2) Estado representado por este nodo.
        self.state: State = state

        # 3) Nodo padre (None si es raíz).
        self.parent: Optional[Node] = parent

        # 4) Acción usada para llegar aquí desde el padre.
        self.action: Optional[Action] = action

        # 5) Costo acumulado desde la raíz.
        #    Aquí asumimos costo uniforme.
        self.path_cost: float = path_cost

        # 6) Profundidad en el árbol.
        self.depth: int = 0 if parent is None else parent.depth + 1

    # ---------------------------------------------------------
    # Generación de sucesores
    # ---------------------------------------------------------

    def expand(self) -> List[Node]:
        """
        Genera todos los nodos hijos (sucesores) desde este nodo.

        Ya no recibe 'problem' como parámetro porque:
        - self.problem fue almacenado en el constructor.
        """

        # 1) Pedimos al problema las acciones válidas
        #    desde el estado actual.
        actions: List[Action] = self.problem.actions(self.state)

        # 2) Por cada acción válida, creamos un hijo.
        children: List[Node] = []
        for action in actions:
            child = self.child_node(action)
            children.append(child)

        return children

    def child_node(self, action: Action) -> Node:
        """
        Crea un único nodo hijo aplicando 'action'.

        Flujo:
        - Calculamos el siguiente estado.
        - Sumamos el costo (+1).
        - Construimos nuevo Node enlazado a este como parent.
        """

        # 1) Calculamos el estado siguiente usando el problema concreto.
        next_state: State = self.problem.result(self.state, action)

        # 2) Como no estamos usando path_cost del problema,
        #    asumimos costo uniforme de 1 por movimiento.
        next_cost: float = self.path_cost + 1

        # 3) Creamos el nodo hijo.
        return Node(
            problem=self.problem,
            state=next_state,
            parent=self,
            action=action,
            path_cost=next_cost,
        )

    # ---------------------------------------------------------
    # Reconstrucción de camino
    # ---------------------------------------------------------

    def path(self) -> List[Node]:
        """
        Retorna la lista de nodos desde la raíz hasta este nodo.

        No necesita acceso al problema.
        """

        node: Optional[Node] = self
        nodes: List[Node] = []

        # Subimos por la cadena de padres.
        while node is not None:
            nodes.append(node)
            node = node.parent

        # Actualmente está en orden inverso.
        nodes.reverse()
        return nodes

    def solution(self) -> List[Action]:
        """
        Retorna únicamente la secuencia de acciones
        desde la raíz hasta este nodo.
        """

        # path()[0] es la raíz (action=None).
        return [n.action for n in self.path()[1:] if n.action is not None]

    # Representación para depuración
    # ---------------------------------------------------------
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"<Node state={self.state} "
            f"cost={self.path_cost} "
            f"depth={self.depth}>"
        )