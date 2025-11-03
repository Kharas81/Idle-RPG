"""
API für BattleEngine: Stellt Endpunkte für Kampfstart, Kampfschritt und Statusabfrage bereit.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


from fastapi import Depends, Query
from rpg_project.src.services.battle_engine import BattleStore, EntityState, BattleStatus


router = APIRouter()
battle_store = BattleStore()

class StartBattleRequest(BaseModel):
    player: EntityState
    opponent: EntityState

@router.post("/battle/start", response_model=BattleStatus)
def start_battle(req: StartBattleRequest, battle_id: str = Query(..., description="ID für den Kampf")):
    return battle_store.create_battle(battle_id, req.player, req.opponent)

@router.post("/battle/step")
def battle_step(battle_id: str = Query(..., description="ID für den Kampf")):
    try:
        return battle_store.step(battle_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Battle step failed: {str(e)}")

@router.get("/battle/state", response_model=BattleStatus)
def battle_state(battle_id: str = Query(..., description="ID für den Kampf")):
    state = battle_store.get_state(battle_id)
    if not state:
        raise HTTPException(status_code=404, detail="Kein Kampf aktiv")
    return state
