from fastapi import APIRouter, Body
import json5
from rpg_project.src.services.dungeon_generator import DungeonGenerator

router = APIRouter()

with open("config/dungeon_rules.json5", "r") as f:
    DUNGEON_CONFIG = json5.load(f)

generator = DungeonGenerator(DUNGEON_CONFIG)

@router.post("/dungeon/enter")
def enter_dungeon(seed: int = Body(...)):
    dungeon = generator.generate(seed)
    return {"dungeon": dungeon}
