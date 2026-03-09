from typing import List, Tuple, TypeAlias, Literal
# Esta clase define la interfaz: actions, result, goal_test, path_cost, etc.

# --------------------------------------------
# Tipos del dominio
# --------------------------------------------

# Cada posicion puede ser 0 (LEFT) o 1 (RIGHT).
Side: TypeAlias = Literal[0, 1]

# Estado = (F, L, O, C) con cada valor 0/1.
State: TypeAlias = Tuple[Side, Side, Side, Side]

# Acciones permitidas
Action: TypeAlias = Literal["F", "FL", "FO", "FC"]

class LoboOvejaColProblem():
    """
    Problema clásico: Granjero (F), Lobo (L), Oveja (O), Col (C).

    Estado: (F, L, O, C) donde cada valor es:
        0 = Izquierda
        1 = Derecha

    Meta: (1, 1, 1, 1)
    """

    # Constantes para que el código sea legible (evitar "números mágicos").
    LEFT: Side = 0
    RIGHT: Side = 1

    def __init__(self) -> None:
        # Estado inicial: todos a la izquierda.
        self.initial: State = (self.LEFT, self.LEFT, self.LEFT, self.LEFT)

        # Estado objetivo: todos a la derecha.
        self.goal: State = (self.RIGHT, self.RIGHT, self.RIGHT, self.RIGHT)

    def actions(self, state: State) -> List[Action]:
        """
        Retorna una lista de acciones válidas desde 'state'.

        Parámetro:
            state: tupla (F, L, O, C) con valores 0/1.

        Retorna:
            Lista de strings: ["F", "FL", "FO", "FC"] (pero solo las aplicables y seguras).
        """
        f, l, o, c = state  # Desempaquetamos la tupla para trabajar cómodo.

        # Siempre es posible que el granjero cruce solo (siempre hay bote con él).
        candidates: List[Action] = ["F"]

        # Si el lobo está en la misma orilla que el granjero, puede llevarlo.
        if l == f:
            candidates.append("FL")

        # Si la oveja está en la misma orilla que el granjero, puede llevarla.
        if o == f:
            candidates.append("FO")

        # Si la col está en la misma orilla que el granjero, puede llevarla.
        if c == f:
            candidates.append("FC")

        # Filtramos acciones que llevan a estados inválidos (inseguros).
        valid_actions: List[Action] = []
        for action in candidates:
            next_state = self.result(state, action)   # simulamos el movimiento
            if self._is_safe(next_state):             # verificamos reglas del puzzle
                valid_actions.append(action)

        return valid_actions
    
    # -----------------------------------------------------
    # Transición de estado
    # -----------------------------------------------------

    def result(self, state, action) -> State:
        """
        Retorna el estado resultante de aplicar 'action' en 'state'.

        Parámetros:
            state: (F, L, O, C)
            action: "F", "FL", "FO" o "FC"

        Retorna:
            next_state: (F', L', O', C') tras cruzar el río.
        """
        f, l, o, c = state  # estado actual

        # Función local para "cambiar de orilla": 0->1 o 1->0.
        def flip(side: Side) -> Side:
            return 1 - side

        # El granjero siempre cruza.
        f2: Side = flip(f)

        # Por defecto, si cruza solo, los demás no cambian.
        l2: Side = l
        o2: Side = o
        c2: Side = c

        # Si la acción incluye pasajero, ese pasajero cruza con el granjero.
        if action == "FL":
            l2 = flip(l)
        elif action == "FO":
            o2 = flip(o)
        elif action == "FC":
            c2 = flip(c)
        elif action == "F":
            pass
        else:
            # Si llega una acción desconocida, es error de modelado.
            raise ValueError(f"Acción inválida: {action}")

        return (f2, l2, o2, c2)

    def goal_test(self, state) -> bool:
        """
        Opcional: podríamos usar el goal_test por defecto de Problem
        (que compara state == self.goal), pero lo dejamos explícito.

        Parámetro:
            state: estado a evaluar.

        Retorna:
            True si state es meta, False si no.
        """
        return state == self.goal

    def _is_safe(self, state) -> bool:
        """
        Helper interno (no es parte de Problem). Reglas de seguridad:

        - Si Lobo y Oveja están juntos sin Granjero -> inválido.
        - Si Oveja y Col están juntos sin Granjero -> inválido.

        Parámetro:
            state: (F, L, O, C)

        Retorna:
            True si es seguro/permitido, False si es inválido.
        """
        f, l, o, c = state

        wolf_eats_sheep = (l == o) and (f != o)
        sheep_eats_cabbage = (o == c) and (f != o)

        return not (wolf_eats_sheep or sheep_eats_cabbage)