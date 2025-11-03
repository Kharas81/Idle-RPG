import unittest
from rpg_project.src.models.ecs import EntityManager, PositionComponent, MoveIntentComponent
from rpg_project.src.services.world_state import WorldState
from rpg_project.src.systems.movement_system import MovementSystem
from rpg_project.src.models.enums import TickMode

class TestECSAndSystems(unittest.TestCase):

    def setUp(self):
        self.world_state = WorldState()
        self.movement_system = MovementSystem()

    def test_entity_creation_and_components(self):
        entity_id = self.world_state.entity_manager.create_entity()
        self.world_state.entity_manager.add_component(entity_id, PositionComponent(0, 0))
        position = self.world_state.entity_manager.get_component(entity_id, PositionComponent)
        self.assertIsNotNone(position)
        self.assertEqual(position.x, 0)
        self.assertEqual(position.y, 0)

    def test_movement_system(self):
        entity_id = self.world_state.entity_manager.create_entity()
        self.world_state.entity_manager.add_component(entity_id, PositionComponent(1, 1))
        self.world_state.entity_manager.add_component(entity_id, MoveIntentComponent(1, 0))

        self.movement_system.update(self.world_state)

        position = self.world_state.entity_manager.get_component(entity_id, PositionComponent)
        self.assertEqual(position.x, 2)
        self.assertEqual(position.y, 1)

if __name__ == "__main__":
    unittest.main()