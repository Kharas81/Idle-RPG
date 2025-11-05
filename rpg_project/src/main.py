# FastAPI-App und API-Router für Battle-API
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from rpg_project.src.api import router as api_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)

# Optional: GameLoop als Funktion erhalten
def run_gameloop():
    from rpg_project.src.models.world import Tile, WorldMap
    from rpg_project.src.services.movement_service import MovementService
    world = WorldMap(
        width=5,
        height=5,
        tiles=[
            Tile(x=0, y=0, type="start"),
            Tile(x=1, y=0, type="floor"),
            Tile(x=2, y=0, type="wall"),
            Tile(x=3, y=0, type="goal"),
            Tile(x=1, y=1, type="floor"),
            Tile(x=2, y=1, type="floor"),
            Tile(x=3, y=1, type="wall"),
        ],
        start=(0, 0),
        goal=(3, 0),
        name="Testmap"
    )
    pos = world.start
    print(f"Startposition: {pos}")
    for direction in ["right", "right", "right"]:
        new_pos = MovementService.move(world, pos, direction)
        print(f"Move {direction}: {pos} -> {new_pos}")
        pos = new_pos
    print(f"Endposition: {pos}")

if __name__ == "__main__":
    # Standard: Starte FastAPI-Server
    import uvicorn
    uvicorn.run("rpg_project.src.main:app", host="0.0.0.0", port=8000, reload=True)
    # Optional: GameLoop-Demo
    # run_gameloop()
