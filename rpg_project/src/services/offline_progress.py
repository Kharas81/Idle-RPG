import time
from typing import Dict
import json5

# Lädt Regeln für Offline-Fortschritt aus der Config
def load_offline_rules():
    with open("config/game_rules.json5", "r") as f:
        rules = json5.load(f)
        return rules.get("offline_progress", {})

class OfflineProgressCalculator:
    def __init__(self):
        self.rules = load_offline_rules()

    def calculate(self, last_logout: float, now: float) -> Dict:
        minutes = int((now - last_logout) // 60)
        max_minutes = self.rules.get("max_offline_minutes", 720)
        minutes = min(minutes, max_minutes)
        xp_per_min = self.rules.get("xp_per_minute", 1)
        gold_per_min = self.rules.get("gold_per_minute", 1)
        resources_per_min = self.rules.get("resources_per_minute", 0)
        return {
            "minutes": minutes,
            "xp": minutes * xp_per_min,
            "gold": minutes * gold_per_min,
            "resources": minutes * resources_per_min
        }

calculator = OfflineProgressCalculator()
