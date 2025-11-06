from rpg_project.src.models.reputation import ReputationState, Faction
from rpg_project.src.services.config_loader import ConfigLoader
from rpg_project.src.models.enums import EventType

class ReputationManager:
    def __init__(self, factions_path="config/factions.json5"):
        self.factions = {f.id: f for f in ConfigLoader.load_config(factions_path, Faction)}
        # Spieler-ID -> ReputationState
        self._reputation = {}

    def get_reputation(self, character_id: str) -> ReputationState:
        if character_id not in self._reputation:
            # Initialisiere mit Startwerten
            self._reputation[character_id] = ReputationState(
                reputation={f_id: f.start_reputation for f_id, f in self.factions.items()}
            )
        return self._reputation[character_id]

    def handle_event(self, event_type, data: dict):
        # Akzeptiere sowohl EventType-Enum als auch String-Namen
        try:
            ev = event_type if isinstance(event_type, EventType) else EventType(event_type)
        except Exception:
            # Ungültiger Event-Type -> ignorieren
            return

        # Beispiel: ON_ENEMY_DEFEATED
        if ev == EventType.ON_ENEMY_DEFEATED:
            char_id = data.get("character_id")
            opponent = data.get("opponent")  # Dict mit "faction"-Feld
            if not opponent or "faction" not in opponent:
                return
            defeated_faction = opponent["faction"]
            # +1 für Fraktionen, die Feinde der besiegten Fraktion sind, -1 für die besiegte Fraktion
            for f_id, faction in self.factions.items():
                if hasattr(faction, "enemies") and defeated_faction in (faction.enemies or []):
                    self.get_reputation(char_id).change(f_id, +1)
            self.get_reputation(char_id).change(defeated_faction, -1)

    def get_api_state(self, character_id: str):
        rep = self.get_reputation(character_id)
        return {f_id: rep.get(f_id) for f_id in self.factions}
