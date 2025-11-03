import logging

logger = logging.getLogger("uvicorn.error")

from fastapi import APIRouter, HTTPException, Depends, FastAPI
from rpg_project.src.services.session_manager import SessionManager
from rpg_project.src.services.world_state import WorldState

router = APIRouter()
session_manager = SessionManager()
world_state = WorldState()

@router.on_event("startup")
def startup_event():
    session_manager.init_database()

@router.post("/session/new")
def create_new_session(ws: WorldState = Depends(lambda: world_state)):
    try:
        session_manager.init_database()
        return {"message": "New session created successfully."}
    except Exception as e:
        logger.error(f"Error in create_new_session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/session/save")
def save_session(ws: WorldState = Depends(lambda: world_state)):
    try:
        session_manager.save_game(world_state)
        return {"message": "Session saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/session/load")
def load_session(ws: WorldState = Depends(lambda: world_state)):
    try:
        session_manager.load_game(world_state)
        return {"message": "Session loaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def create_app(world_state):
    app = FastAPI()
    app.include_router(router)

    # Pass world_state directly to endpoints via dependency injection
    @app.on_event("startup")
    async def startup_event():
        global session_manager
        session_manager = SessionManager()

    return app