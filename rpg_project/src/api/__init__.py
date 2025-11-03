"""
API-Router-Registrierung für alle API-Module (inkl. battle.py)
"""
from fastapi import APIRouter
from rpg_project.src.api import battle, game_state, replay

router = APIRouter()
router.include_router(battle.router)
router.include_router(game_state.router)
router.include_router(replay.router)
