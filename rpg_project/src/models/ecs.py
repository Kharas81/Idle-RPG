class EntityManager:
    def __init__(self):
        self._next_entity_id = 1
        self._entities = set()
        self._components = {}

    def create_entity(self):
        entity_id = self._next_entity_id
        self._next_entity_id += 1
        self._entities.add(entity_id)
        self._components[entity_id] = {}
        return entity_id

    def add_component(self, entity_id, component):
        if entity_id not in self._entities:
            raise ValueError(f"Entity {entity_id} does not exist.")
        self._components[entity_id][type(component)] = component

    def get_component(self, entity_id, component_type):
        return self._components[entity_id].get(component_type)

    def remove_component(self, entity_id, component_type):
        if entity_id in self._components:
            self._components[entity_id].pop(component_type, None)