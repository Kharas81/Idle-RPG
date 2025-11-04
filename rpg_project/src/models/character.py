from typing import Any

from pydantic import BaseModel, Field


class Character(BaseModel):
    """Repräsentiert einen RPG-Charakter mit XP, Level, Gold, Inventar, Ausrüstung und Stats.
    """

    id: str
    name: str
    level: int = 1
    xp: int = 0
    gold: int = 0
    inventory: list[dict[str, Any]] = Field(default_factory=list)
    equipment: dict[str, str] = Field(default_factory=dict)  # z.B. {"weapon": "sword_01"}
    stats: dict[str, int] = Field(default_factory=dict)      # z.B. {"ATK": 5, "DEF": 2}
    talents: list[str] = Field(default_factory=list)         # Liste der freigeschalteten Talent-IDs
    percent_bonuses: dict[str, float] = Field(default_factory=dict)  # z.B. {"fire": 0.1}
