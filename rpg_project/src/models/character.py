from typing import List, Dict, Any
from pydantic import BaseModel, Field

class Character(BaseModel):
    """
    Repräsentiert einen RPG-Charakter mit XP, Level, Gold und Inventar.
    """
    name: str
    level: int = 1
    xp: int = 0
    gold: int = 0
    inventory: List[Dict[str, Any]] = Field(default_factory=list)
    # Weitere Attribute wie HP, ATK, DEF etc. können später ergänzt werden
