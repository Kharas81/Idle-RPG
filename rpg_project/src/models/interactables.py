"""Datenmodell für interaktive Objekte (z.B. Truhen, Türen, Schalter) auf der Karte.
Alle Werte werden aus der Map-Config geladen.
"""
from enum import Enum
from typing import Any

from pydantic import BaseModel


class InteractableType(str, Enum):
    CHEST = "chest"
    DOOR = "door"
    SWITCH = "switch"
    # Erweiterbar für weitere Typen

class InteractableState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    LOCKED = "locked"
    USED = "used"
    # Erweiterbar

class Interactable(BaseModel):
    id: str  # Eindeutige ID auf der Map
    type: InteractableType
    position: tuple[int, int]  # (x, y) Koordinaten auf der Map
    state: InteractableState = InteractableState.CLOSED
    loot: list[str] | None = None  # Item-IDs, die enthalten sind (z.B. in Truhe)
    properties: dict[str, Any] | None = None  # Zusätzliche Daten (z.B. Schlüssel-ID, Schalter-Ziel)

    class Config:
        use_enum_values = True
