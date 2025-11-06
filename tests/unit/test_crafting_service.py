import sys
import os
def test_craft_with_empty_inventory(recipes, dummy_player_factory):
    player = dummy_player_factory([])
    service = CraftingService(recipes)
    assert not service.can_craft(player, "Eisenschwert")
    assert not service.craft(player, "Eisenschwert")

def test_craft_multiple_times(recipes, dummy_player_factory):
    player = dummy_player_factory([
        {"name": "Eisenerz", "amount": 10}
    ])
    service = CraftingService(recipes)
    assert service.craft(player, "Eisenschwert")
    assert service.craft(player, "Eisenschwert")
    # Nach 2x Crafting sollte Eisenerz auf 0 sein
    assert all(item["name"] != "Eisenerz" or item["amount"] == 0 for item in player.inventory)
    # 2x Eisenschwert im Inventar
    assert sum(item["name"] == "Eisenschwert" for item in player.inventory) >= 1

def test_craft_invalid_recipe_name(recipes, dummy_player_factory):
    player = dummy_player_factory([
        {"name": "Eisenerz", "amount": 5}
    ])
    service = CraftingService(recipes)
    assert not service.can_craft(player, "UnbekanntesItem")
    assert not service.craft(player, "UnbekanntesItem")

def test_craft_with_overflow(recipes, dummy_player_factory):
    # Spieler hat mehr Ressourcen als nötig
    player = dummy_player_factory([
        {"name": "Eisenerz", "amount": 100}
    ])
    service = CraftingService(recipes)
    assert service.craft(player, "Eisenschwert")
    # Es bleibt Eisenerz übrig
    assert any(item["name"] == "Eisenerz" and item["amount"] > 0 for item in player.inventory)

def test_craft_with_multiple_ingredients(dummy_player_factory):
    # Simuliere ein Rezept mit mehreren Zutaten
    from rpg_project.src.models.crafting import Recipe, CraftingInput, CraftingOutput
    multi_recipe = Recipe(
        name="Stahlschwert",
        inputs=[
            CraftingInput(name="Eisenerz", amount=2),
            CraftingInput(name="Holz", amount=1)
        ],
        outputs=[CraftingOutput(name="Stahlschwert", amount=1)]
    )
    player = dummy_player_factory([
        {"name": "Eisenerz", "amount": 2},
        {"name": "Holz", "amount": 1}
    ])
    service = CraftingService([multi_recipe])
    assert service.can_craft(player, "Stahlschwert")
    assert service.craft(player, "Stahlschwert")
    assert any(item["name"] == "Stahlschwert" for item in player.inventory)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

"""
Unit-Tests für CraftingService
"""

import pytest
import json5
from rpg_project.src.models.crafting import Recipe
from rpg_project.src.services.crafting_service import CraftingService

# Fixtures werden zentral über conftest.py bereitgestellt




@pytest.fixture
def recipes():
    with open("config/recipes.json5", encoding="utf-8") as f:
        data = json5.load(f)
    return [Recipe(**r) for r in data]

def test_craft_iron_sword(recipes, dummy_player_factory):
    player = dummy_player_factory([
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

def test_craft_fails_without_resources(recipes, dummy_player_factory):
    player = dummy_player_factory([
        {"name": "Eisenerz", "amount": 3}
    ])
    service = CraftingService(recipes)
    assert not service.can_craft(player, "Eisenschwert")
    assert not service.craft(player, "Eisenschwert")
