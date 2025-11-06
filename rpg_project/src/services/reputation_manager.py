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

    def handle_event(self, event_type: str, data: dict):
        # Beispiel: ON_ENEMY_DEFEATED
        if event_type == EventType.ON_ENEMY_DEFEATED:
            char_id = data["character_id"]
            opponent = data["opponent"]  # Dict mit "faction"-Feld
            if not opponent or "faction" not in opponent:
                return
            defeated_faction = opponent["faction"]
            # +1 für Feinde der besiegten Fraktion, -1 für besiegte Fraktion
            for f_id, faction in self.factions.items():
                if defeated_faction in faction.enemies:
                    self.get_reputation(char_id).change(f_id, +1)
            self.get_reputation(char_id).change(defeated_faction, -1)

    def get_api_state(self, character_id: str):
        rep = self.get_reputation(character_id)
        return {f_id: rep.get(f_id) for f_id in self.factions}
