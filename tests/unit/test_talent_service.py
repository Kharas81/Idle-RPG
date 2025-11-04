"""
Unit-Tests für TalentService
"""
import pytest
from rpg_project.src.services.talent_service import TalentService
from rpg_project.src.models.character import Character
from rpg_project.src.models.talent import Talent, TalentEffect, TalentTree

@pytest.fixture
def fire_mastery_talent():
    return Talent(
        id="fire_mastery",
        name="Feuermagie-Meisterschaft",
        description="+10% Feuerschaden für alle Feuer-Skills.",
        effects=[TalentEffect(effect_type="percent_bonus", target="fire", value=0.1)],
        prerequisites=[],
    )

@pytest.fixture
def strength_training_talent():
    return Talent(
        id="strength_training",
        name="Krafttraining",
        description="+2 Angriff.",
        effects=[TalentEffect(effect_type="stat_bonus", target="ATK", value=2)],
        prerequisites=[],
    )

@pytest.fixture
def talent_tree(fire_mastery_talent, strength_training_talent):
    return TalentTree(talents={
        "fire_mastery": fire_mastery_talent,
        "strength_training": strength_training_talent,
    })

@pytest.fixture
def character():
    return Character(name="Held", stats={"ATK": 5}, equipment={})

def test_learn_stat_bonus_talent(talent_tree, character):
    service = TalentService(talent_tree)
    assert service.learn_talent(character, "strength_training")
    assert "strength_training" in character.talents
    assert character.stats["ATK"] == 7

def test_learn_percent_bonus_talent(talent_tree, character):
    service = TalentService(talent_tree)
    assert service.learn_talent(character, "fire_mastery")
    assert "fire_mastery" in character.talents
    assert hasattr(character, "percent_bonuses")
    assert character.percent_bonuses["fire"] == 0.1

def test_cannot_learn_twice(talent_tree, character):
    service = TalentService(talent_tree)
    assert service.learn_talent(character, "fire_mastery")
    assert not service.learn_talent(character, "fire_mastery")

def test_cannot_learn_without_prerequisite():
    # Talent mit Voraussetzung
    t1 = Talent(id="t1", name="A", description="", effects=[], prerequisites=[])
    t2 = Talent(id="t2", name="B", description="", effects=[], prerequisites=["t1"])
    tree = TalentTree(talents={"t1": t1, "t2": t2})
    char = Character(name="Held", stats={}, equipment={})
    service = TalentService(tree)
    assert not service.learn_talent(char, "t2")
    assert service.learn_talent(char, "t1")
    assert service.learn_talent(char, "t2")
