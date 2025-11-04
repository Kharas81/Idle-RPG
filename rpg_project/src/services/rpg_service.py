import json
import os
from typing import Any

from rpg_project.src.models.character import Character


class RPGService:
    """Reagiert auf RPG-Events (z.B. ON_ENEMY_DEFEATED) und verwaltet XP, Gold, Level-Ups und Inventar.
    """

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "../../../config/game_rules.json5")
        self.xp_curve = self._load_xp_curve(config_path)

    def _load_xp_curve(self, path: str):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data.get("xp_curve", [0, 100, 300, 600, 1000])  # Default XP-Kurve

    def handle_event(self, event: str, character: Character, data: dict[str, Any]) -> Character:
        if event == "ON_ENEMY_DEFEATED":
            xp_gain = data.get("xp", 0)
            gold_gain = data.get("gold", 0)
            loot = data.get("loot", [])
            character.xp += xp_gain
            character.gold += gold_gain
            character.inventory.extend(loot)
            # Level-Up prüfen
            while character.level < len(self.xp_curve) and character.xp >= self.xp_curve[character.level]:
                character.level += 1
        return character
