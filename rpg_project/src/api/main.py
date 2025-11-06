
"""
main.py
Initialisiert die FastAPI-App und registriert alle modularisierten Router für das Idle-RPG.
Stellt sicher, dass der globale game_state in allen Modulen verfügbar ist.
"""

from fastapi import FastAPI

from rpg_project.src.api.game_state import router as game_state_router, game_state
from rpg_project.src.api.game_state_movement import router as movement_router
from rpg_project.src.api.game_state_battle import router as battle_router
from rpg_project.src.api.game_state_inventory import router as inventory_router
from rpg_project.src.api.game_state_tickreset import router as tickreset_router
from rpg_project.src.api.reputation import router as reputation_router

app = FastAPI()

# Setze den globalen game_state für alle API-Module
import rpg_project.src.api.game_state_movement as movement
import rpg_project.src.api.game_state_battle as battle
import rpg_project.src.api.game_state_inventory as inventory
import rpg_project.src.api.game_state_tickreset as tickreset
for mod in (movement, battle, inventory, tickreset):
	mod.game_state = game_state

# Registriere alle modularisierten Router
for router in (movement_router, battle_router, inventory_router, tickreset_router, game_state_router, reputation_router):
	app.include_router(router, prefix="/api")
