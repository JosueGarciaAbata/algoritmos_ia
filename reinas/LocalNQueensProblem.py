from typing import List, Tuple
import random

State = list[int]
Action = Tuple[int, int]  # (columna, nueva_fila)


class LocalNQueensProblem:
    def __init__(self, n: int):
        self.n = n
        self.initial_state: State = self.random_state(n)

    def actions(self, state: State) -> List[Action]:
        actions = []
        for col in range(self.n):
            for new_row in range(self.n):
                if state[col] != new_row:
                    actions.append((col, new_row))
        return actions

    def result(self, state: State, action: Action) -> State:
        new_state = state.copy()
        col, new_row = action
        new_state[col] = new_row
        return new_state

    # Funcion de costo
    def conflicts(self, state: State) -> int:
        conflicts = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    # Fitness function
    def value(self, state: State) -> int:
        return -self.conflicts(state)

    def random_state(self, n: int) -> State:
        return [random.randint(0, n - 1) for _ in range(n)]