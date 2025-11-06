from pydantic import BaseModel
from typing import List, Optional

class PetSkill(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    power: int
    cooldown: int

class PetStats(BaseModel):
    hp: int
    atk: int
    defense: int
    speed: int

class Pet(BaseModel):
    id: str
    name: str
    type: str  # z.B. "Wolf", "Golem"
    stats: PetStats
    skills: List[PetSkill]
    ai_policy: Optional[str] = None  # z.B. "aggressive", "defensive"
