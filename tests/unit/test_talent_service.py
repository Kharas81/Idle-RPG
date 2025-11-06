def test_learn_invalid_talent_name(talent_tree, character):
    service = TalentService(talent_tree)
    assert not service.learn_talent(character, "unbekanntes_talent")

def test_learn_talent_with_cycle(talent_factory, character_factory):
    # Zyklische Voraussetzungen: t1 -> t2 -> t1
    t1 = talent_factory(id="t1", name="A", description="", effect_type="stat_bonus", target="ATK", value=1, prerequisites=["t2"])
    t2 = talent_factory(id="t2", name="B", description="", effect_type="stat_bonus", target="ATK", value=1, prerequisites=["t1"])
    tree = TalentTree(talents={"t1": t1, "t2": t2})
    char = character_factory(id="testchar4", name="Held", stats={"ATK": 1})
    service = TalentService(tree)
    # Sollte nicht erlernbar sein, da Zyklus
    assert not service.learn_talent(char, "t1")
    assert not service.learn_talent(char, "t2")

def test_learn_talent_with_nested_prerequisites(talent_factory, character_factory):
    # Verschachtelte Voraussetzungen: t1 -> t2 -> t3
    t3 = talent_factory(id="t3", name="C", description="", effect_type="stat_bonus", target="ATK", value=1)
    t2 = talent_factory(id="t2", name="B", description="", effect_type="stat_bonus", target="ATK", value=1, prerequisites=["t3"])
    t1 = talent_factory(id="t1", name="A", description="", effect_type="stat_bonus", target="ATK", value=1, prerequisites=["t2"])
    tree = TalentTree(talents={"t1": t1, "t2": t2, "t3": t3})
    char = character_factory(id="testchar5", name="Held", stats={"ATK": 1})
    service = TalentService(tree)
    # t1 nicht ohne t2, t2 nicht ohne t3
    assert not service.learn_talent(char, "t1")
    assert not service.learn_talent(char, "t2")
    assert service.learn_talent(char, "t3")
    assert service.learn_talent(char, "t2")
    assert service.learn_talent(char, "t1")

def test_learn_talent_character_without_stats(talent_tree, character_factory):
    char = character_factory(id="testchar6", name="Held", stats=None)
    service = TalentService(talent_tree)
    # Sollte robust gegen fehlende Stats sein
    assert not service.learn_talent(char, "strength_training")
"""
Unit-Tests für TalentService
"""

import pytest
from rpg_project.src.models.talent import TalentTree, Talent
from rpg_project.src.services.talent_service import TalentService

# Fixtures und Models werden zentral über conftest.py bereitgestellt


@pytest.fixture
def fire_mastery_talent(talent_factory):
    return talent_factory(
        id="fire_mastery",
        name="Feuermagie-Meisterschaft",
        description="+10% Feuerschaden für alle Feuer-Skills.",
        effect_type="percent_bonus",
        target="fire",
        value=0.1,
        prerequisites=[],
    )

@pytest.fixture
def strength_training_talent(talent_factory):
    return talent_factory(
        id="strength_training",
        name="Krafttraining",
        description="+2 Angriff.",
        effect_type="stat_bonus",
        target="ATK",
        value=2,
        prerequisites=[],
    )

@pytest.fixture
def talent_tree(fire_mastery_talent, strength_training_talent):
    return TalentTree(talents={
        "fire_mastery": fire_mastery_talent,
        "strength_training": strength_training_talent,
    })

@pytest.fixture
def character(character_factory):
    return character_factory(id="testchar2", name="Held", stats={"ATK": 5}, equipment={})

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
    char = Character(id="testchar3", name="Held", stats={}, equipment={})
    service = TalentService(tree)
    assert not service.learn_talent(char, "t2")
    assert service.learn_talent(char, "t1")
    assert service.learn_talent(char, "t2")
