from abstracciones.Node import Node


def depth_limited_search(problem, limit):
    """
    Realiza una búsqueda en profundidad con límite de profundidad.

    Este algoritmo funciona como una búsqueda en profundidad, pero
    solo permite descender hasta un nivel máximo dado por `limit`.

    Puede devolver tres tipos de resultado:
    - Node: si encuentra el estado objetivo
    - 'cutoff': si la búsqueda se detuvo por alcanzar el límite
    - None: si no encontró solución en las ramas exploradas

    Args:
        problem:
            Problema de búsqueda que define el estado inicial, las acciones
            posibles, la transición entre estados y la prueba de meta.

        limit:
            Profundidad máxima que la búsqueda puede explorar.

    Returns:
        Un nodo solución si encuentra la meta, 'cutoff' si el límite impidió
        seguir explorando, o None si no existe solución en el subárbol revisado.
    """

    def recursive_dls(node, limit):

        # Si encontramos el objetivo
        if problem.goal_test(node.state):
            return node

        # Si alcanzamos el límite de profundidad
        elif limit == 0:
            return 'cutoff'

        else:
            cutoff_occurred = False

            # Expandir los hijos del nodo
            for child in node.expand(problem=problem):
                result = recursive_dls(child, limit - 1)

                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result

            # Si alguna rama alcanzó el límite devolvemos cutoff
            return 'cutoff' if cutoff_occurred else None

    root = Node(state=problem.initial_state)
    return recursive_dls(root, limit)


def iterative_deepening_search(problem):
    """
    Realiza una búsqueda en profundidad iterativa.

    Este algoritmo ejecuta varias búsquedas con límite de profundidad,
    comenzando desde 0 e incrementando el límite gradualmente:
    0, 1, 2, 3, ...

    La idea es combinar:
    - la poca memoria de la búsqueda en profundidad
    - la completitud de la búsqueda en anchura

    En cada iteración se llama a `depth_limited_search` con un nuevo
    límite, hasta encontrar la solución o determinar que no existe.

    Args:
        problem:
            Problema de búsqueda que define el estado inicial, las acciones
            posibles, la transición entre estados y la prueba de meta.

    Returns:
        Un nodo solución si encuentra la meta, o None si no existe solución.
    """

    depth = 0

    while True:
        result = depth_limited_search(problem, depth)

        # Si no fue cutoff, entonces encontramos solución o no existe
        if result != 'cutoff':
            return result

        depth += 1