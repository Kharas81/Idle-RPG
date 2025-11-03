from pydantic import BaseModel, Field
from typing import List, Optional
from .enums import ItemType, Rarity, OpponentType, Element

class Item(BaseModel):
    id: str
    name: str
    type: ItemType
    rarity: Rarity
    description: Optional[str] = None
    value: int = 0
    effects: Optional[List[str]] = None

class Opponent(BaseModel):
    id: str
    name: str
    type: OpponentType
    level: int
    hp: int
    attack: int
    defense: int
    element: Element = Element.PHYSICAL
    loot_table: Optional[List[str]] = None
    description: Optional[str] = None
