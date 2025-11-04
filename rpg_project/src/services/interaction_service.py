"""Service für Interaktionen mit interaktiven Objekten (z.B. Truhen öffnen, Loot erhalten).
Bindet an das Event-System an und ist datengetrieben (Map-Config).
"""
from typing import Any

from rpg_project.src.models.character import Character
from rpg_project.src.models.interactables import Interactable, InteractableState, InteractableType
from rpg_project.src.services.event_manager import EventManager


class InteractionService:
    def __init__(self, event_manager: EventManager, interactables: dict[str, Interactable]):
        """:param event_manager: Zentrales Event-System
        :param interactables: Dict aller Interactables auf der Map (id -> Interactable)
        """
        self.event_manager = event_manager
        self.interactables = interactables

    def interact(self, character: Character, interactable_id: str) -> dict[str, Any]:
        """Führt eine Interaktion mit einem Objekt aus (z.B. Truhe öffnen).
        Gibt das Ergebnis als dict zurück (z.B. erhaltene Items).
        """
        if interactable_id not in self.interactables:
            return {"success": False, "error": "Object not found"}
        obj = self.interactables[interactable_id]
        if obj.type == InteractableType.CHEST:
            return self._open_chest(character, obj)
        # Weitere Typen (Tür, Schalter) können hier ergänzt werden
        return {"success": False, "error": "Unknown interactable type"}

    def _open_chest(self, character: Character, chest: Interactable) -> dict[str, Any]:
        if chest.state == InteractableState.OPEN:
            return {"success": False, "error": "Chest already open"}
        if chest.state == InteractableState.LOCKED:
            return {"success": False, "error": "Chest is locked"}
        loot = chest.loot or []
        # Füge Loot dem Inventar hinzu (vereinfachtes Beispiel)
        if hasattr(character, "inventory") and isinstance(character.inventory, list):
            character.inventory.extend(loot)
        else:
            character.inventory = list(loot)
        chest.state = InteractableState.OPEN
        # Event publizieren
        self.event_manager.publish("ON_CHEST_OPENED", {"character_id": character.id, "chest_id": chest.id, "loot": loot})
        return {"success": True, "loot": loot}
