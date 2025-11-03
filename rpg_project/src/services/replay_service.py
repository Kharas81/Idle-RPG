"""
ReplayService: Speichert und lädt Replay-Daten (Seed, Aktionen) für deterministische Runs.
"""
from typing import List, Dict, Any

class ReplayService:
    def __init__(self):
        self._replay_data: Dict[str, Any] = {}

    def save(self, seed: int, actions: List[Any]) -> Dict[str, Any]:
        self._replay_data = {"seed": seed, "actions": actions}
        return self._replay_data

    def load(self) -> Dict[str, Any]:
        return self._replay_data

    def reset(self):
        self._replay_data = {}

# Singleton-Instanz
replay_service = ReplayService()
