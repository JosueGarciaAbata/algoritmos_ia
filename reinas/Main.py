
from reinas.LocalNQueensProblem import LocalNQueensProblem
from reinas.HillClimbing import hill_climbing
from reinas.Node import Node
from reinas.HillClimbingStochastic import hill_climbing as hill_climbing_stochastic
from reinas.TempleSimulado import temple_simulado

if __name__ == "__main__":
    
    problem = LocalNQueensProblem(n=8)
    # result_node: Node = hill_climbing(problem)
    # result_node: Node = hill_climbing_stochastic(problem)
    result_node: Node = temple_simulado(problem)

    print("Estado inicial:", problem.initial_state)
    print("Estado final:", result_node.state)
    print("Conflictos en el estado final:", problem.conflicts(result_node.state))

    pass