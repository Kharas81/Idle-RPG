"""API-Endpunkt: /character/learn_talent
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from rpg_project.src.models.character import Character
from rpg_project.src.models.talent import Talent, TalentTree
from rpg_project.src.services.config_loader import ConfigLoader
from rpg_project.src.services.talent_service import TalentService

router = APIRouter()

active_character = Character(id="dummychar2", name="Held", stats={"ATK": 5}, equipment={})
# Lade Talente aus Config
raw_talents = ConfigLoader.load_config("config/talents.json5", Talent)
talent_tree = TalentTree(talents={t.id: t for t in raw_talents})
talent_service = TalentService(talent_tree)

class LearnTalentRequest(BaseModel):
    talent_id: str

@router.post("/character/learn_talent")
def learn_talent(req: LearnTalentRequest):
    success = talent_service.learn_talent(active_character, req.talent_id)
    if not success:
        raise HTTPException(status_code=400, detail="Talent konnte nicht freigeschaltet werden.")
    return {"success": True, "talents": getattr(active_character, "talents", []), "stats": active_character.stats, "percent_bonuses": getattr(active_character, "percent_bonuses", {})}
