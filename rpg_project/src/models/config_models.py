from pydantic import BaseModel
from typing import List
from .enums import ItemType, OpponentType

class ItemConfig(BaseModel):
    id: str
    name: str
    type: ItemType
    effects: List[str]

class OpponentConfig(BaseModel):
    id: str
    name: str
    type: OpponentType
    health: int