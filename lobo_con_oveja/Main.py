from LoboConOvejaProblema import (
  LoboOvejaColProblem,
  State
)
from BFSTreeLocoConOveja import breadth_first_tree_search
from typing import List

if __name__ == "__main__":

  problem = LoboOvejaColProblem()
  goal_node =  breadth_first_tree_search(problem)

  if goal_node is None:
    print("No se encontró solución.")
  else:

    plan = goal_node.solution()
    print("Plan encontrado:")
    states: List[State] = [n.state for n in goal_node.path()]

    print("Estado inicial: ", problem.initial)
    print("Estado objetivo: ", problem.goal)
    print("\nPlan de acciones:", plan)
    print("Numero de pasos:", len(plan))

    print("\nCamino recorrido:")
    for i, state in enumerate(states):
      print(f"  Paso {i + 1}: {state}")