"""API-Endpunkt für Interaktionen mit Objekten (z.B. Truhe öffnen).
POST /action/interact
"""
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from rpg_project.src.models.character import Character
from rpg_project.src.models.interactables import Interactable
from rpg_project.src.services.event_manager import EventManager
from rpg_project.src.services.interaction_service import InteractionService

router = APIRouter()

# Dummy-Storage für Demo-Zwecke (in echt: aus GameState laden)
INTERACTABLES: dict[str, Interactable] = {}
EVENT_MANAGER = EventManager()
INTERACTION_SERVICE = InteractionService(EVENT_MANAGER, INTERACTABLES)

class InteractRequest(BaseModel):
    character_id: str
    interactable_id: str

@router.post("/action/interact")
def interact_with_object(req: InteractRequest) -> dict[str, Any]:
    # In echt: Character aus GameState laden
    character = Character(id=req.character_id, name="Test", inventory=[])
    result = INTERACTION_SERVICE.interact(character, req.interactable_id)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Unknown error"))
    return result
