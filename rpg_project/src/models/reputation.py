from pydantic import BaseModel
from typing import Dict, List

class Faction(BaseModel):
    id: str
    name: str
    description: str
    start_reputation: int = 0
    enemies: List[str] = []

class ReputationState(BaseModel):
    # Aktueller Ruf pro Fraktion
    reputation: Dict[str, int]  # faction_id -> reputation

    def get(self, faction_id: str) -> int:
        return self.reputation.get(faction_id, 0)

    def set(self, faction_id: str, value: int):
        self.reputation[faction_id] = value

    def change(self, faction_id: str, delta: int):
        self.reputation[faction_id] = self.get(faction_id) + delta
