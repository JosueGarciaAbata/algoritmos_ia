from puzzle.Puzzle8Problem import Puzzle8Problem
from informadas.AStar import AStar

if __name__ == "__main__":

  problem: Puzzle8Problem = Puzzle8Problem()
  goal_node = AStar(problem, lambda node: node.path_cost + problem.manhattan_distance(node))

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
