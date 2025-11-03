from rpg_project.src.models.enums import TickMode
from rpg_project.src.services.world_state import WorldState

class GameLoop:
    def __init__(self, world_state: WorldState):
        self.world_state = world_state

    def tick(self, mode: TickMode):
        if mode == TickMode.REALTIME:
            print("Running in REALTIME mode")
            # Call all systems, including visual and sound systems
        elif mode == TickMode.SIMULATION:
            print("Running in SIMULATION mode")
            # Call only core logic systems like movement and battle

if __name__ == "__main__":
    world_state = WorldState()
    game_loop = GameLoop(world_state)
    game_loop.tick(TickMode.SIMULATION)