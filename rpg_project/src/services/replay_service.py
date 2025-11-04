"""ReplayService: Speichert und lädt Replay-Daten (Seed, Aktionen) für deterministische Runs.
"""
from typing import Any


class ReplayService:
    def __init__(self):
        self._replay_data: dict[str, Any] = {}

    def save(self, seed: int, actions: list[Any]) -> dict[str, Any]:
        self._replay_data = {"seed": seed, "actions": actions}
        return self._replay_data

    def load(self) -> dict[str, Any]:
        return self._replay_data

    def reset(self):
        self._replay_data = {}

# Singleton-Instanz
replay_service = ReplayService()
