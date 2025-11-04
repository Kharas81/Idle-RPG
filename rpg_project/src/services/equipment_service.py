"""
EquipmentService

Verwaltet das Anlegen und Ablegen von Ausrüstung und berechnet die modifizierten Charakterwerte.
"""
from typing import Dict, Optional
from rpg_project.src.models.character import Character
from rpg_project.src.models.enums import EquipmentSlot

class EquipmentService:
    def __init__(self, items_config: Dict[str, dict]):
        """
        items_config: Dict mit allen Item-Definitionen aus config/items.json5
        """
        self.items_config = items_config

    def equip(self, character: Character, item_id: str) -> bool:
        """
        Legt ein Item an (z.B. Eisenschwert). Gibt True zurück, wenn erfolgreich.
        """
        item_data = self.items_config.get(item_id)
        if not item_data:
            return False
        slot = item_data["slot"]
        # Falls Slot schon belegt, erst ablegen
        if character.equipment.get(slot):
            self.unequip(character, slot)
        character.equipment[slot] = item_id
        self._apply_stats(character, item_data["stats"])
        return True

    def unequip(self, character: Character, slot: str) -> bool:
        """
        Legt das Item im Slot ab. Gibt True zurück, wenn erfolgreich.
        """
        item_id = character.equipment.get(slot)
        if not item_id:
            return False
        item_data = self.items_config.get(item_id)
        if item_data:
            self._remove_stats(character, item_data["stats"])
        character.equipment.pop(slot)
        return True

    def _apply_stats(self, character: Character, stats: Dict[str, int]):
        for stat, value in stats.items():
            character.stats[stat] = character.stats.get(stat, 0) + value

    def _remove_stats(self, character: Character, stats: Dict[str, int]):
        for stat, value in stats.items():
            character.stats[stat] = character.stats.get(stat, 0) - value
            if character.stats[stat] <= 0:
                character.stats.pop(stat)

    def get_equipped_items(self, character: Character) -> Dict[str, str]:
        return character.equipment.copy()
