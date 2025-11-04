import json
import os
from threading import Lock
from typing import Any


class SessionManager:
    """Verwaltet das Speichern und Laden von Spielständen (Sessions).
    Speichert pro Session eine JSON-Datei im Verzeichnis 'sessions/'.
    """

    _instance = None
    _lock = Lock()
    SESSIONS_DIR = os.path.join(os.path.dirname(__file__), "../../../sessions")

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                os.makedirs(cls.SESSIONS_DIR, exist_ok=True)
            return cls._instance

    def new_session(self, session_id: str, initial_state: dict[str, Any]) -> None:
        """Erzeugt eine neue Session mit Startzustand."""
        path = self._get_session_path(session_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(initial_state, f, ensure_ascii=False, indent=2)

    def save_session(self, session_id: str, state: dict[str, Any]) -> None:
        """Speichert den aktuellen Zustand der Session."""
        path = self._get_session_path(session_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def load_session(self, session_id: str) -> dict[str, Any] | None:
        """Lädt den Zustand der Session. Gibt None zurück, falls nicht vorhanden."""
        path = self._get_session_path(session_id)
        if not os.path.exists(path):
            return None
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def _get_session_path(self, session_id: str) -> str:
        return os.path.join(self.SESSIONS_DIR, f"{session_id}.json")
