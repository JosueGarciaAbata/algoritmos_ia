import math
import random
from reinas.LocalNQueensProblem import LocalNQueensProblem
from reinas.Node import Node


def temple_simulado(problem: LocalNQueensProblem) -> Node:
    current = Node(state=problem.initial_state)
    schedule = exp_schedule(k=20, lam=0.005, limit=1000)

    for t in range(1, 1001):
        T = schedule(t)

        if T == 0:
            return current

        neighbors = current.expand(problem)
        next_choice = random.choice(neighbors)

        # Recordemos: menos conflictos el valor es mas alto; mas conflictos el valor es mas bajo.
        delta_e = problem.value(next_choice.state) - problem.value(current.state)

        if delta_e > 0:
            current = next_choice
        else:
            prob_e = math.exp(delta_e / T)

            if random.random() < prob_e:
                current = next_choice

    return current


def exp_schedule(k=20, lam=0.005, limit=1000):
    return lambda t: (k * math.exp(-lam * t) if t < limit else 0)