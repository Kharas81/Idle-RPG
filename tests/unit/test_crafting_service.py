import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import json5
import pytest

from rpg_project.src.models.crafting import Recipe
from rpg_project.src.services.crafting_service import CraftingService


class DummyPlayer:
    def __init__(self, inventory):
        self.inventory = inventory

@pytest.fixture
def recipes():
    with open("config/recipes.json5", encoding="utf-8") as f:
        data = json5.load(f)
    return [Recipe(**r) for r in data]

def test_craft_iron_sword(recipes):
    player = DummyPlayer([
        {"name": "Eisenerz", "amount": 5}
    ])
    service = CraftingService(recipes)
    assert service.can_craft(player, "Eisenschwert")
    success = service.craft(player, "Eisenschwert")
    assert success
    # Eisenerz abgezogen
    assert all(item["name"] != "Eisenerz" or item["amount"] == 0 for item in player.inventory)
    # Eisenschwert im Inventar
    assert any(item["name"] == "Eisenschwert" and item["amount"] == 1 for item in player.inventory)

def test_craft_fails_without_resources(recipes):
    player = DummyPlayer([
        {"name": "Eisenerz", "amount": 3}
    ])
    service = CraftingService(recipes)
    assert not service.can_craft(player, "Eisenschwert")
    assert not service.craft(player, "Eisenschwert")
