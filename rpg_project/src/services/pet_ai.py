from rpg_project.src.models.pet import Pet
from typing import Dict, Any

class PetAI:
    def __init__(self, pet: Pet):
        self.pet = pet
        self.state: Dict[str, Any] = {}

    def decide_action(self, battle_context: Dict[str, Any]) -> str:
        # Sehr einfaches Beispiel: Wähle immer den ersten Skill
        if self.pet.skills:
            return self.pet.skills[0].id
        return "wait"
