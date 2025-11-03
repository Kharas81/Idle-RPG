from rpg_project.src.models.ecs import EntityManager
from rpg_project.src.models.config_models import MapConfig

class WorldState:
    def __init__(self):
        self.entity_manager = EntityManager()
        self.current_map: MapConfig = None

    def set_map(self, map_config: MapConfig):
        self.current_map = map_config

    def tick(self):
        # Placeholder for game loop tick logic
        pass