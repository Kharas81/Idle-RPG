from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from rpg_project.src.services.session_manager import SessionManager
from typing import Dict, Any

router = APIRouter()
session_manager = SessionManager()

class NewSessionRequest(BaseModel):
    session_id: str
    initial_state: Dict[str, Any]

class SaveSessionRequest(BaseModel):
    session_id: str
    state: Dict[str, Any]

@router.post("/session/new")
def new_session(req: NewSessionRequest):
    session_manager.new_session(req.session_id, req.initial_state)
    return {"status": "ok", "msg": f"Session {req.session_id} created."}

@router.post("/session/save")
def save_session(req: SaveSessionRequest):
    session_manager.save_session(req.session_id, req.state)
    return {"status": "ok", "msg": f"Session {req.session_id} saved."}

@router.get("/session/load")
def load_session(session_id: str):
    state = session_manager.load_session(session_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "ok", "session_id": session_id, "state": state}
