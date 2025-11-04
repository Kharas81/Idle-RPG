
from pydantic import BaseModel


class TileType(str):
    WALL = "wall"
    FLOOR = "floor"
    START = "start"
    GOAL = "goal"

class Tile(BaseModel):
    x: int
    y: int
    type: str  # wall, floor, start, goal

class WorldMap(BaseModel):
    width: int
    height: int
    tiles: list[Tile]
    start: tuple[int, int]
    goal: tuple[int, int]
    name: str | None = None
