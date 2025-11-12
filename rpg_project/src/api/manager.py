"""
API-Endpunkte für Manager-Agent und RL-Training
"""
from fastapi import APIRouter, Body
from typing import Optional

router = APIRouter()

@router.post("/train/{agent}")
def train_agent(agent: str):
    # Dummy: Training starten (Fighter/Explorer)
    # Hier würde das RL-Training angestoßen werden
    return {"status": "Training gestartet", "agent": agent}

@router.post("/manager/mode")
def set_manager_mode(mode: str = Body(..., embed=True)):
    # Dummy: Modus setzen (auto/manual)
    # Hier würde der Manager-Agent umgeschaltet werden
    return {"status": "Modus gesetzt", "mode": mode}

@router.post("/manager/override")
def set_agent_override(agent: Optional[str] = Body(None, embed=True)):
    # Dummy: Aktiven Agenten setzen (Explorer/Fighter)
    # Hier würde der Manager-Agent den aktiven Spezialagenten wechseln
    return {"status": "Override gesetzt", "agent": agent}
