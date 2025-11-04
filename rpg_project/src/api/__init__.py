"""API-Router-Registrierung für alle API-Module (inkl. battle.py)
"""
from fastapi import APIRouter


from rpg_project.src.api import battle, game_state, replay, session, equipment, interaction, stats, talent


router = APIRouter()
router.include_router(battle.router)
router.include_router(game_state.router)
router.include_router(replay.router)
router.include_router(session.router)
router.include_router(equipment.router)
router.include_router(interaction.router)
router.include_router(stats.router)
router.include_router(talent.router)
