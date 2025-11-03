from pydantic import BaseModel
from typing import List, Tuple, Optional

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
    tiles: List[Tile]
    start: Tuple[int, int]
    goal: Tuple[int, int]
    name: Optional[str] = None
