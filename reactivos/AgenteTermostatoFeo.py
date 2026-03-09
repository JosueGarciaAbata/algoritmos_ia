import random

HEAT = "HEAT"
COOL = "COOL"
NOOP = "NOOP"


class ThermostatEnvironment:
    """
    Entorno mínimo (clases, pero 'feo'):
    - Estado: current_temp
    - Objetivo: target_temp
    - Percepto: current_temp
    - Acciones: HEAT / COOL / NOOP
    """
    def __init__(self, start_temp: int, target_temp: int) -> None:
        self.current_temp = start_temp
        self.target_temp = target_temp

    def percept(self) -> int:
        # No hay agente genérico: el entorno solo entrega un percepto simple.
        return self.current_temp

    def execute_action(self, action: str) -> None:
        # El entorno aplica la acción (reglas del mundo)
        if action == HEAT:
            self.current_temp += 1
        elif action == COOL:
            self.current_temp -= 1
        elif action == NOOP:
            pass
        else:
            raise ValueError(f"Invalid action: {action}")

        # Ruido del entorno (opcional). Comenta esta línea si quieres determinismo.
        self.current_temp += random.choice([-1, 0, 1])

    def is_done(self) -> bool:
        return self.current_temp == self.target_temp

    def step(self, brain) -> tuple[str, int]:
        # “Feo”: acoplado a que brain tenga .program(percept) -> action
        p = self.percept()
        a = brain.program(p)
        self.execute_action(a)
        return a, p


class ReflexThermostatAgent:
    """Agente reflejo simple: sin memoria, solo reglas."""
    def __init__(self, target_temp: int) -> None:
        self.target_temp = target_temp

    def program(self, percept_temp: int) -> str:
        if percept_temp < self.target_temp:
            return HEAT
        if percept_temp > self.target_temp:
            return COOL
        return NOOP


if __name__ == "__main__":
    env = ThermostatEnvironment(start_temp=15, target_temp=20)
    brain = ReflexThermostatAgent(target_temp=20)

    for t in range(1, 21):
        action, percept = env.step(brain)
        print(f"Step {t:02d}: Percept={percept}, Action={action}, CurrentTemp={env.current_temp}")

        if env.is_done():
            print(f"Target temperature reached in {t} steps!")
            break