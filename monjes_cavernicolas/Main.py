from monjes_cavernicolas.MonjesCavernicolasProblema import MonjesCavernicolasProblema

from abstracciones.Problem import Problem
from abstracciones.Node import Node

from no_informadas.BFSTree import breadth_first_tree_search
from no_informadas.DFSTree import depth_first_tree_search
from no_informadas.DFSGraph import depth_first_graph_search
from no_informadas.BFSGraph import breadth_first_graph_search
from no_informadas.BidirectionalBFSGraph import bidirectional_breadth_first_graph_search
from no_informadas.IDDFSGraph import iterative_deepening_search

from informadas.UCS import uniform_cost_search

if __name__ == "__main__":

  problem: Problem = MonjesCavernicolasProblema()
  goal_node = depth_first_graph_search(problem)

  if goal_node is None:
    print("No se encontró solución.")
  else:

    plan = goal_node.solution()
    print("\nPlan encontrado:")

    states: list = [n.state for n in goal_node.path()]

    print("Estado inicial: ", problem.initial_state)
    print("Estado objetivo: ", problem.goal_state)
    print("\nPlan de acciones:", plan)

    print("\nCamino recorrido:")
    for i, state in enumerate(states):
      print(f"  Paso {i + 1}: {state}")

    print ("Profundidad del nodo objetivo: ", goal_node.depth)
    print("Coste del camino: ", goal_node.path_cost)