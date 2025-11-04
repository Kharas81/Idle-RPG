"""
Talentmodell für den Talentbaum
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class TalentEffect(BaseModel):
    effect_type: str  # z.B. 'stat_bonus', 'skill_bonus', 'percent_bonus'
    target: str       # z.B. 'fireball', 'ATK', 'all_skills'
    value: float      # z.B. 0.1 für +10%
    description: Optional[str] = None

class Talent(BaseModel):
    id: str
    name: str
    description: str
    effects: List[TalentEffect]
    prerequisites: List[str] = []  # IDs anderer Talente

class TalentTree(BaseModel):
    talents: Dict[str, Talent]  # talent_id -> Talent
    # Optional: Struktur für Visualisierung/Verzweigungen
