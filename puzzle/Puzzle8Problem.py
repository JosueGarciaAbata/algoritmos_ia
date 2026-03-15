
from abstracciones.Node import Node
from abstracciones.Problem import Problem

State = list[list[int]]  # Representación del estado del puzzle como una matriz 3x3
Action: str # Las acciones pueden ser 'up', 'down', 'left', 'right' para mover el espacio vacío (0)

class Puzzle8Problem(Problem):
    def __init__(self):
        super().__init__(
            initial_state=[[7, 2, 4], [5, 0, 6], [8, 3, 1]],  # Estado inicial del puzzle
            goal_state=[[0, 1, 2], [3, 4, 5], [6, 7, 8]]  # Estado objetivo del puzzle
        )

    def actions(self, state: State) -> list[str]:
        # Aquí se implementaría la lógica para generar las acciones válidas desde el estado dado.

        # Las acciones válidas dependen de la posición del espacio vacío (0) en el estado actual.
        zero_row, zero_col = self.find_zero_position(state)
        possible_actions: list[str] = []

        if zero_row > 0:
            possible_actions.append('up')
        if zero_row < 2:
            possible_actions.append('down')
        if zero_col > 0:
            possible_actions.append('left')
        if zero_col < 2:
            possible_actions.append('right')

        return possible_actions

    def result(self, state: State, action: str) -> State:
        # Implementar la lógica para mover el espacio vacío (0) según la acción
        # y devolver el nuevo estado resultante.

        if action not in ['up', 'down', 'left', 'right']:
            raise ValueError("Acción no válida. Debe ser 'up', 'down', 'left' o 'right'.")
        
        # Encontrar el espacio vacío (0) en el estado actual
        zero_row, zero_col = self.find_zero_position(state)
        new_row, new_col = zero_row, zero_col

        # Verificar que la posicion del espacio vacío (0) se pueda mover en la dirección indicada.
        if action == "up":
            new_row = zero_row - 1

        elif action == 'down':
            new_row = zero_row + 1

        elif action == 'left':
            new_col = zero_col - 1

        elif action == 'right':
            new_col = zero_col + 1
        
        new_state = [row[:] for row in state]

        # Intercambiar el espacio vacío (0) con el número en la nueva posición.
        new_state[zero_row][zero_col] = state[new_row][new_col]
        new_state[new_row][new_col] = 0

        return new_state
            
    def find_zero_position(self, state: State) -> tuple[int, int]:
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 0:
                    return i, j
        raise ValueError("El espacio vacío (0) no se encontró en el estado.")
    
    def is_safe(self, state: State) -> bool:
        # En el caso del 8-puzzle, todos los estados generados por acciones válidas son seguros,
        # ya que no hay restricciones adicionales como en otros problemas.
        return True
    
    def manhattan_distance(self, node: Node) -> int:
        total = 0
        for i in range(len(node.state)):
            for j in range(len(node.state[i])):
                value = node.state[i][j]
                if value != 0:
                    goal_row, goal_col = self.find_goal_position(value)
                    total += abs(i - goal_row) + abs(j - goal_col)
        return total

    def find_goal_position(self, value: int) -> tuple[int, int]:
        for i in range(len(self.goal_state)):
            for j in range(len(self.goal_state[i])):
                if self.goal_state[i][j] == value:
                    return i, j
        raise ValueError(f"El valor {value} no se encontró en el estado objetivo.")