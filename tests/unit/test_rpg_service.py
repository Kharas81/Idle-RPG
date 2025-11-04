
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from rpg_project.src.models.character import Character
from rpg_project.src.services.rpg_service import RPGService

def test_on_enemy_defeated_xp_gold_levelup():
    # Arrange
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../config/game_rules.json5'))
    rpg = RPGService(config_path)
    char = Character(name="TestHero")
    # Simuliere: Gegner gibt 120 XP, 50 Gold, 1 Loot
    event_data = {"xp": 120, "gold": 50, "loot": [{"item_id": "potion", "qty": 1}]}
    # Act
    char = rpg.handle_event("ON_ENEMY_DEFEATED", char, event_data)
    # Assert
    assert char.xp == 120
    assert char.gold == 50
    assert char.level == 2  # Level 2 ab 100 XP laut game_rules.json5
    assert char.inventory == [{"item_id": "potion", "qty": 1}]

    # Noch ein Gegner: 200 XP, 10 Gold, 2 Loot
    event_data2 = {"xp": 200, "gold": 10, "loot": [{"item_id": "sword", "qty": 1}, {"item_id": "coin", "qty": 5}]}
    char = rpg.handle_event("ON_ENEMY_DEFEATED", char, event_data2)
    assert char.xp == 320
    assert char.gold == 60
    assert char.level == 3  # Level 3 ab 300 XP laut game_rules.json5
    assert char.inventory == [
        {"item_id": "potion", "qty": 1},
        {"item_id": "sword", "qty": 1},
        {"item_id": "coin", "qty": 5}
    ]


def test_no_levelup_if_xp_too_low():
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../config/game_rules.json5'))
    rpg = RPGService(config_path)
    char = Character(name="LowXP")
    event_data = {"xp": 50, "gold": 5, "loot": []}
    char = rpg.handle_event("ON_ENEMY_DEFEATED", char, event_data)
    assert char.level == 1
    assert char.xp == 50
    assert char.gold == 5
    assert char.inventory == []
