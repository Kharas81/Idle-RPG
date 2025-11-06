from fastapi import APIRouter, Body
from pydantic import BaseModel
from rpg_project.src.services.dialogue_manager import dialogue_manager

router = APIRouter()

class DialogueRequest(BaseModel):
    npc_id: str
    node_id: str = None
    option_id: str = None

@router.post("/npc/talk")
def start_dialogue(request: DialogueRequest = Body(...)):
    node = dialogue_manager.start_dialogue(request.npc_id)
    if not node:
        return {"error": "NPC nicht gefunden"}
    return node.dict()

@router.post("/npc/dialogue_choice")
def choose_dialogue_option(request: DialogueRequest = Body(...)):
    node = dialogue_manager.choose_option(request.npc_id, request.node_id, request.option_id)
    if not node:
        return {"end": True}
    return node.dict()
