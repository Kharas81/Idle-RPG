from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class Entity(BaseModel):
    type: str
    x: int
    y: int
    hp: int
    max_hp: int
    atk: int
    def_: int
    inventory: Optional[List[Dict[str, Any]]] = None
    skills: Optional[List[str]] = None
    effects: Optional[List[str]] = None

class GameState(BaseModel):
    width: int
    height: int
    tiles: List[Dict[str, Any]]
    entities: List[Dict[str, Any]]
    tick: int
    world_seed: Optional[int] = None
    meta: Optional[Dict[str, Any]] = None
