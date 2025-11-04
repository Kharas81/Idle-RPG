"""OpponentAI: Gegner-KI-Logik für verschiedene Verhaltenstypen.
- Entscheidet, welche Aktion ein Gegner im Kampf ausführt (z.B. Angriff, Flucht, Skill-Nutzung)
- Liest ai_policy aus der Opponent-Config
"""
from typing import Any


class OpponentAI:
    def __init__(self, ai_policy: dict[str, Any]):
        self.ai_policy = ai_policy

    def decide_action(self, opponent_state, battle_state) -> str:
        """Gibt die nächste Aktion zurück: "attack", "flee", "skill:<name>"
        """
        # Beispiel: Flucht bei niedrigem Leben
        if self.ai_policy.get("type") == "coward":
            hp_percent = opponent_state.hp / opponent_state.max_hp
            if hp_percent <= self.ai_policy.get("flee_threshold", 0.2):
                return "flee"
        # Standard: Angriff
        return "attack"
