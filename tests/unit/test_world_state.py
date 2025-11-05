import pytest
from rpg_project.src.services.world_state import WorldState

@pytest.fixture
def world_state():
    return WorldState()

def test_add_and_remove_component(world_state):
    entity_id = world_state.entity_manager.create_entity()

    class TestComponent:
        pass

    component = TestComponent()
    world_state.add_component(entity_id, component)
    retrieved_component = world_state.entity_manager.get_component(entity_id, TestComponent)
    assert retrieved_component is component

    world_state.remove_component(entity_id, TestComponent)
    retrieved_component = world_state.entity_manager.get_component(entity_id, TestComponent)
    assert retrieved_component is None