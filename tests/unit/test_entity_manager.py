import pytest
from rpg_project.src.models.ecs import EntityManager

@pytest.fixture
def entity_manager():
    return EntityManager()

def test_create_entity(entity_manager):
    entity_id = entity_manager.create_entity()
    assert entity_id == 1

def test_add_and_get_component(entity_manager):
    entity_id = entity_manager.create_entity()

    class TestComponent:
        pass

    component = TestComponent()
    entity_manager.add_component(entity_id, component)
    retrieved_component = entity_manager.get_component(entity_id, TestComponent)
    assert retrieved_component is component

def test_remove_component(entity_manager):
    entity_id = entity_manager.create_entity()

    class TestComponent:
        pass

    component = TestComponent()
    entity_manager.add_component(entity_id, component)
    entity_manager.remove_component(entity_id, TestComponent)
    retrieved_component = entity_manager.get_component(entity_id, TestComponent)
    assert retrieved_component is None