
from typing import Any, Optional, Dict
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
import time
from rpg_project.src.services.session_manager import SessionManager
from rpg_project.src.services.offline_progress import calculator

router = APIRouter()
session_manager = SessionManager()
USER_DB: Dict[str, Dict[str, Optional[float]]] = {"player1": {"last_logout": None}}



class LoginRequest(BaseModel):
    username: str



class LogoutRequest(BaseModel):
    username: str



@router.post("/session/login")
def session_login(request: LoginRequest = Body(...)):
    user = USER_DB.get(request.username)
    now = time.time()
    if user and user["last_logout"] is not None:
        result = calculator.calculate(user["last_logout"], now)
        user["last_logout"] = None  # Reset
        return {"offline_reward": result}
    return {"offline_reward": None}



@router.post("/session/logout")
def session_logout(request: LogoutRequest = Body(...)):
    user = USER_DB.setdefault(request.username, {"last_logout": None})
    user["last_logout"] = time.time()
    return {"ok": True}



class NewSessionRequest(BaseModel):
    session_id: str
    initial_state: dict[str, Any]



class SaveSessionRequest(BaseModel):
    session_id: str
    state: dict[str, Any]


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


class LoginRequest(BaseModel):
    username: str

class LogoutRequest(BaseModel):
    username: str

@router.post("/session/login")

