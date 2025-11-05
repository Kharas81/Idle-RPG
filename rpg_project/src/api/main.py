from fastapi import FastAPI
from rpg_project.src.api.game_state import router as game_state_router, game_state
from rpg_project.src.api.game_state_movement import router as movement_router
from rpg_project.src.api.game_state_battle import router as battle_router
from rpg_project.src.api.game_state_inventory import router as inventory_router
from rpg_project.src.api.game_state_tickreset import router as tickreset_router

app = FastAPI()

# Setze game_state für alle Module
import rpg_project.src.api.game_state_movement as movement
import rpg_project.src.api.game_state_battle as battle
import rpg_project.src.api.game_state_inventory as inventory
import rpg_project.src.api.game_state_tickreset as tickreset
movement.game_state = game_state
battle.game_state = game_state
inventory.game_state = game_state
tickreset.game_state = game_state

app.include_router(movement_router, prefix="/api")
app.include_router(battle_router, prefix="/api")
app.include_router(inventory_router, prefix="/api")
app.include_router(tickreset_router, prefix="/api")

# Optional: Hauptrouter für Basis-Endpunkte
app.include_router(game_state_router, prefix="/api")
