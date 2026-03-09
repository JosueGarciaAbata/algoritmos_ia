from abstracciones.Problem import Problem
from typing import TypeAlias, Literal, List, Tuple

Side: TypeAlias = Literal[0, 1]  # 0 para izquierda, 1 para derecha
State: TypeAlias = Tuple[int, int, int]  # (monjes_izquierda, canibales_izquierda, bote_en_izquierda)
Action: TypeAlias = Tuple[int, int]  # (monjes_a_cruzar, canibales_a_cruzar)

class MonjesCavernicolasProblema(Problem):

    def __init__(self) -> None:
        super().__init__(
            initial_state=(3, 3, 0),
            goal_state=(0, 0, 1)
            )

        # Estado inicial: todos los monjes y caníbales a la izquierda.
        # self.initial: State = (3, 3, 0)  # (monjes_izquierda, canibales_izquierda, bote_en_izquierda)

        # Estado objetivo: todos los monjes y caníbales a la derecha.
        # self.goal: State = (0, 0, 1)  # (monjes_izquierda, canibales_izquierda, bote_en_derecha)

    def actions(self, state: State) -> List[Action]:
        # Aquí se implementaría la lógica para generar las acciones válidas desde el estado dado.
        M, C, B = state  # Desempaquetamos el estado para trabajar cómodo.
        possible_actions: List[Action] = []

        # Definimos las posibles combinaciones de monjes y caníbales que pueden cruzar el río.
        for m in range(3):  # 0, 1 o 2 monjes
            for c in range(3):  # 0, 1 o 2 caníbales
                if (m + c >= 1) and (m + c <= 2):  # El bote puede llevar 1 o 2 personas
                    if B == 0:  # El bote está en la izquierda
                        if m <= M and c <= C:  # Verificamos que haya suficientes monjes y caníbales para cruzar
                            possible_actions.append((m, c))  # Acción: (monjes a cruzar, caníbales a cruzar)
                    else:  # El bote está en la derecha
                        if m <= (3 - M) and c <= (3 - C):  # Verificamos que haya suficientes
                            possible_actions.append((m, c))  # Acción: (monjes a cruzar, can
                            # íbales a cruzar)
        
        # Filtramos las acciones que llevarían a estados inseguros (donde los caníbales superan a los monjes en alguna orilla).

        valid_actions: List[Action] = []
        for action in possible_actions:
            next_state = self.result(state, action) # Simulamos el movimiento
            if self.is_safe(next_state):
                valid_actions.append(action)

        return valid_actions

    def result(self, state: State, action: Action) -> State:
        # Aquí se implementaría la lógica para calcular el estado resultante de aplicar una acción al estado dado.

        M, C, B = state  # Desempaquetamos el estado para trabajar cómodo.
        m, c, B = 0, 0, B  # Inicializamos variables para el nuevo estado.

        if B == 0: # El bote esta a la izquierda.
          m = M - action[0] # Monjes que cruzan a la derecha
          c = C - action[1] # Caníbales que cruzan a la derecha
          B = 1 # El bote cruza a la derecha
        else: # El bote esta a la derecha.
          m = M + action[0] # Monjes que cruzan a la izquierda
          c = C + action[1] # Caníbales que cruzan a la izquierda
          B = 0 # El bote cruza a la izquierda
          pass;

        return (m, c, B)

    def is_safe(self, state: State) -> bool:
        # Aquí se implementaría la lógica para verificar si un estado es seguro según las reglas del problema.
        M, C, B = state  # Desempaquetamos el estado para trabajar cómodo.

        if B == 0: # El bote esta a la izquierda.
            if M < C and M > 0: # Si hay más caníbales que monjes en la izquierda, y hay al menos un monje, el estado es inseguro.
                return False

        if B == 1: # El bote esta a la derecha.
            if (3 - M) < (3 - C) and (3 - M) > 0: # Si hay más caníbales que monjes en la derecha, y hay al menos un monje, el estado es inseguro.
                return False

        return True
