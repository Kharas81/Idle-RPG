from typing import Type, Dict, Any, TypeVar, Optional

T = TypeVar('T')

class EntityManager:
    def __init__(self):
        self._next_entity_id = 1
        self._entities = set()
        self.entities = {}  # Dictionary to store entities and their components
        self._components: Dict[int, Dict[Type, Any]] = {}

    def create_entity(self, entity_id=None):
        if entity_id is None:
            entity_id = self._next_entity_id
            self._next_entity_id += 1
        print(f"Creating entity {entity_id}")
        print(f"Entities before creation: {self._entities}")
        if entity_id in self._entities:
            raise ValueError(f"Entity {entity_id} already exists.")
        self._entities.add(entity_id)
        self.entities[entity_id] = {}
        self._components[entity_id] = {}
        print(f"Entities after creation: {self._entities}")
        return entity_id

    def add_component(self, entity_id: int, component: Any):
        if entity_id not in self._entities:
            print(f"Error: Entity {entity_id} does not exist in _entities: {self._entities}")
            raise ValueError(f"Cannot add component. Entity {entity_id} does not exist.")
        if not isinstance(component, object):
            raise TypeError("Component must be an object.")
        self._components[entity_id][type(component)] = component

    def get_component(self, entity_id: int, component_type: Type[T]) -> Optional[T]:
        if entity_id not in self._entities:
            raise ValueError(f"Cannot get component. Entity {entity_id} does not exist.")
        return self._components[entity_id].get(component_type)

    def get_entities_with(self, *component_types: Type) -> Dict[int, Dict[Type, Any]]:
        result = {}
        for entity_id, components in self._components.items():
            if all(ct in components for ct in component_types):
                result[entity_id] = {ct: components[ct] for ct in component_types}
        return result

class PositionComponent:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class MoveIntentComponent:
    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy

class HPComponent:
    def __init__(self, value: int):
        self.value = value

class StatsComponent:
    def __init__(self, hp: int, atk: int, def_: int):
        self.hp = hp
        self.atk = atk
        self.def_ = def_

class InBattleComponent:
    def __init__(self, battle_id: str):
        self.battle_id = battle_id

class ActionRequestComponent:
    def __init__(self, action: dict):
        self.action = action