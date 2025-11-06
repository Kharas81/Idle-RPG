import pytest
from rpg_project.src.services.battle_engine import EntityState
from rpg_project.src.models.talent import Talent, TalentEffect
from rpg_project.src.models.character import Character

@pytest.fixture
def entity_factory():
    def _factory(id, name, hp, max_hp, atk, defense, is_player, **kwargs):
        return EntityState(id=id, name=name, hp=hp, max_hp=max_hp, atk=atk, defense=defense, is_player=is_player, **kwargs)
    return _factory

@pytest.fixture
def dummy_player_factory():
    class DummyPlayer:
        def __init__(self, inventory):
            self.inventory = inventory
    return DummyPlayer

@pytest.fixture
def talent_factory():
    def _factory(id, name, description, effect_type, target, value, prerequisites=None):
        return Talent(
            id=id,
            name=name,
            description=description,
            effects=[TalentEffect(effect_type=effect_type, target=target, value=value)],
            prerequisites=prerequisites or [],
        )
    return _factory

@pytest.fixture
def character_factory():
    def _factory(id, name, stats=None, equipment=None, talents=None):
        return Character(id=id, name=name, stats=stats or {}, equipment=equipment or {}, talents=talents or set())
    return _factory
