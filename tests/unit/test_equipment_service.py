"""Unit-Tests für EquipmentService
"""
import pytest

from rpg_project.src.models.character import Character
from rpg_project.src.services.equipment_service import EquipmentService


@pytest.fixture
def items_config():
    return {
        "sword_01": {
            "id": "sword_01",
            "name": "Eisenschwert",
            "slot": "weapon",
            "stats": {"ATK": 5},
        },
        "armor_01": {
            "id": "armor_01",
            "name": "Lederrüstung",
            "slot": "armor",
            "stats": {"DEF": 2},
        },
    }

@pytest.fixture
def character():
    return Character(id="testchar1", name="Held", stats={"ATK": 1, "DEF": 0}, equipment={})

def test_equip_weapon_increases_atk(items_config, character):
    service = EquipmentService(items_config)
    assert service.equip(character, "sword_01")
    assert character.equipment["weapon"] == "sword_01"
    assert character.stats["ATK"] == 6  # 1 + 5

def test_unequip_weapon_removes_atk(items_config, character):
    service = EquipmentService(items_config)
    service.equip(character, "sword_01")
    assert service.unequip(character, "weapon")
    assert "weapon" not in character.equipment
    assert character.stats["ATK"] == 1

def test_equip_armor_increases_def(items_config, character):
    service = EquipmentService(items_config)
    assert service.equip(character, "armor_01")
    assert character.equipment["armor"] == "armor_01"
    assert character.stats["DEF"] == 2

def test_equip_replaces_existing(items_config, character):
    service = EquipmentService(items_config)
    service.equip(character, "sword_01")
    # Zweites Schwert mit anderem Wert
    items_config["sword_02"] = {
        "id": "sword_02",
        "name": "Stahlschwert",
        "slot": "weapon",
        "stats": {"ATK": 10},
    }
    assert service.equip(character, "sword_02")
    assert character.equipment["weapon"] == "sword_02"
    assert character.stats["ATK"] == 11  # 1 + 10

def test_equip_invalid_item(items_config, character):
    service = EquipmentService(items_config)
    assert not service.equip(character, "not_exist")
    assert "weapon" not in character.equipment

def test_unequip_empty_slot(items_config, character):
    service = EquipmentService(items_config)
    assert not service.unequip(character, "weapon")

def test_unequip_removes_stat_completely(items_config, character):
    service = EquipmentService(items_config)
    service.equip(character, "sword_01")
    service.unequip(character, "weapon")
    assert "ATK" in character.stats  # Grundwert bleibt
    # Jetzt DEF testen, das auf 0 fällt
    service.equip(character, "armor_01")
    service.unequip(character, "armor")
    assert "DEF" not in character.stats

def test_get_equipped_items(items_config, character):
    service = EquipmentService(items_config)
    service.equip(character, "sword_01")
    equipped = service.get_equipped_items(character)
    assert equipped == {"weapon": "sword_01"}
    # Mutationen am Rückgabewert dürfen Original nicht beeinflussen
    equipped["weapon"] = "hacked"
    assert character.equipment["weapon"] == "sword_01"
