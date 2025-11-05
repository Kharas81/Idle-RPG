from rpg_project.src.models.ecs import EntityManager

class WorldState:
    def __init__(self):
        self.entity_manager = EntityManager()

    def add_component(self, entity_id, component):
        self.entity_manager.add_component(entity_id, component)

    def remove_component(self, entity_id, component_type):
        self.entity_manager.remove_component(entity_id, component_type)