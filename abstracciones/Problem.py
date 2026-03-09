class Problem:
    """
    Clase base abstracta para representar un problema de búsqueda.

    Un problema de búsqueda define, como mínimo:

    1. Un estado inicial:
       El punto desde donde comienza el agente.

    2. Un estado objetivo:
       El estado que se desea alcanzar.

    3. Acciones posibles:
       Qué movimientos o decisiones se pueden tomar desde un estado.

    4. Función de transición:
       Qué estado resulta al aplicar una acción.

    Además, opcionalmente, puede definir:

    5. Una prueba de seguridad o validez:
       Para descartar estados inválidos.

    6. Un costo de camino:
       Para problemas donde algunas acciones cuestan más que otras.

    Esta clase no resuelve el problema por sí sola; únicamente describe
    la estructura que un algoritmo de búsqueda necesita para trabajar.

    Las subclases deben implementar al menos `actions` y `result`.
    """

    def __init__(self, initial_state, goal_state):
        """
        Inicializa el problema con un estado inicial y un estado objetivo.

        Args:
            initial_state:
                Estado desde el cual comienza la búsqueda.

            goal_state:
                Estado que se desea alcanzar.
        """
        self.initial_state = initial_state
        self.goal_state = goal_state

    def actions(self, state) -> list:
        """
        Devuelve las acciones válidas que pueden ejecutarse desde `state`.

        Este método debe ser implementado por cada problema concreto,
        ya que las acciones dependen del dominio.

        Args:
            state:
                Estado actual desde el cual se quieren obtener acciones.

        Returns:
            Una colección de acciones válidas para ese estado.

        Raises:
            NotImplementedError:
                Si la subclase no implementa este método.

        Ejemplo:
            En el problema de un laberinto, podría devolver:
            ['arriba', 'abajo', 'izquierda', 'derecha']
            pero solo las que sean posibles desde la posición actual.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def result(self, state, action) -> object:
        """
        Devuelve el nuevo estado que resulta de aplicar `action` sobre `state`.

        Este método representa la dinámica del problema: dado un estado
        actual y una acción, indica a qué estado se llega.

        Args:
            state:
                Estado actual.

            action:
                Acción que se desea aplicar.

        Returns:
            El nuevo estado alcanzado después de ejecutar la acción.

        Raises:
            NotImplementedError:
                Si la subclase no implementa este método.

        Ejemplo:
            Si `state` es la posición (2, 3) y la acción es 'derecha',
            el resultado podría ser (2, 4).
        """
        raise NotImplementedError("Subclasses must implement this method")

    def goal_test(self, state) -> bool:
        """
        Verifica si `state` es un estado objetivo.

        Por defecto, considera que un estado es meta si es igual a
        `self.goal_state`.

        Args:
            state:
                Estado que se desea comprobar.

        Returns:
            True si el estado es la meta; en caso contrario, False.

        Nota:
            Este método puede sobrescribirse en una subclase si el problema
            tiene una condición de meta más compleja que una simple igualdad.

        Ejemplo:
            En algunos problemas puede haber varias metas válidas, o una meta
            definida por una propiedad, no por un único valor exacto.
        """
        return state == self.goal_state

    def is_safe(self, state) -> bool:
        """
        Indica si un estado es válido, permitido o seguro dentro del problema.

        Este método es útil en problemas donde no basta con generar estados:
        también hay que descartar aquellos que violan restricciones.

        Args:
            state:
                Estado que se desea validar.

        Returns:
            True si el estado es seguro o válido; False si debe descartarse.

        Raises:
            NotImplementedError:
                Si la subclase no implementa este método.

        Ejemplo:
            En el problema de misioneros y caníbales, un estado no es seguro
            si en alguna orilla hay más caníbales que misioneros y todavía
            hay misioneros presentes.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def path_cost(self, cost_so_far, state1, action, state2) -> float:
        """
        Calcula el costo acumulado de un camino al pasar de `state1`
        a `state2` mediante `action`.

        Args:
            cost_so_far:
                Costo acumulado del camino hasta `state1`.

            state1:
                Estado de origen.

            action:
                Acción aplicada para pasar de `state1` a `state2`.

            state2:
                Estado resultante.

        Returns:
            El nuevo costo acumulado del camino.

        Comportamiento por defecto:
            Esta implementación asume que cada acción cuesta 1.
            Por tanto, el costo total simplemente aumenta en una unidad.

        Nota:
            Este método puede sobrescribirse si algunas acciones cuestan
            más que otras.

        Ejemplo:
            - En un problema de grafo simple, cada arista puede costar 1.
            - En un mapa de ciudades, moverse entre ciudades puede tener
              costos distintos según la distancia.
        """
        return cost_so_far + 1