"""Talentmodell für den Talentbaum
"""
from pydantic import BaseModel



from typing import Optional, Union, Any

class TalentEffect(BaseModel):
    effect_type: str  # z.B. 'stat_bonus', 'skill_bonus', 'percent_bonus', 'unlock_skill', ...
    target: Optional[str] = None  # z.B. 'fireball', 'ATK', 'all_skills', kann fehlen
    value: Optional[Union[float, str, bool]] = None  # Kann Zahl, String, bool oder None sein
    description: Optional[str] = None
    chance: Optional[float] = None
    # Für maximale Flexibilität: weitere Felder erlaubt
    extra: dict[str, Any] = {}

    class Config:
        extra = "allow"

class Talent(BaseModel):
    id: str
    name: str
    description: str
    effects: list[TalentEffect]
    prerequisites: list[str] = []  # IDs anderer Talente

class TalentTree(BaseModel):
    talents: dict[str, Talent]  # talent_id -> Talent
    # Optional: Struktur für Visualisierung/Verzweigungen
