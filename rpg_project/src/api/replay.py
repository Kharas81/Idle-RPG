"""
API für Replay- und RNG-Service: Seed setzen, Replay speichern/laden
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Any
from rpg_project.src.services.rng_service import rng_service
from rpg_project.src.services.replay_service import replay_service

router = APIRouter()

class SetSeedRequest(BaseModel):
    seed: int

class SaveReplayRequest(BaseModel):
    actions: List[Any]

@router.post("/rng/seed")
def set_seed(req: SetSeedRequest):
    rng_service.seed(req.seed)
    return {"seed": req.seed}

@router.post("/replay/save")
def save_replay(req: SaveReplayRequest):
    seed = rng_service.get_seed()
    if seed is None:
        raise HTTPException(status_code=400, detail="Seed nicht gesetzt")
    data = replay_service.save(seed, req.actions)
    return data

@router.post("/replay/load")
def load_replay():
    data = replay_service.load()
    if not data:
        raise HTTPException(status_code=404, detail="Kein Replay gespeichert")
    # Seed zurücksetzen
    rng_service.seed(data["seed"])
    return data
