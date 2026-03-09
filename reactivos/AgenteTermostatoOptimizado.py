from dataclasses import dataclass

HEAT = "HEAT"
COOL = "COOL"
NOOP = "NOOP"

@dataclass
class Agent:
  program: callable[[int], str]
  name: str = "Agent"

class ThermostateEnvironment:
  """
  Entorno minimo:
  - Estado del mundo: temperatura (int)
  - Percepto: temperatura actual
  - Acciones: HEAT / COOL / NOOP
  """

  def __init__(self, start_temp: int, target_temp: int) -> None:
    self.current_temp = start_temp
    self.target_temp = target_temp

  def percept(self, agent: Agent) -> int:
    return self.current_temp
  
  def execute_action(self, agent: Agent, action: str) -> None:
    if (action == HEAT):
      self.current_temp += 1
    elif (action == COOL):
      self.current_temp -= 1
    elif (action == NOOP):
      pass
    else:
      raise ValueError(f"Invalid action: {action}")
    
  def is_done(self) -> bool:
    return self.current_temp == self.target_temp
  
  def step(self, agent: Agent) -> tuple[str, int]:
    percept = self.percept(agent)
    action = agent.program(percept)
    self.execute_action(agent, action)
    return action, percept

class ReflexThermostatAgent: 
  """
  Agente reflejo simple: decide SOLO con el percepto actual (sin memoria).
  """
  def __init__(self, target_temp: int) -> None:
    self.target_temp = target_temp

  def program(self, percept_temp: int) -> str:
    if percept_temp < self.target_temp:
      return HEAT
    elif percept_temp > self.target_temp:
      return COOL
    return NOOP
  
if __name__ == "__main__":

  env = ThermostateEnvironment(start_temp=15, target_temp=20)
  brain = ReflexThermostatAgent(target_temp=20)
  agent = Agent(program=brain.program, name="ThermostatAgent")

  for t in range(1, 21):
    action, percept = env.step(agent)
    print(f"Step {t}: Percept={percept}, Action={action}, Current Temp={env.current_temp}")

    if env.is_done():
      print(f"Target temperature reached in {t} steps!")
      break