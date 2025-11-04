
from pydantic import BaseModel

from .enums import Element, ItemType, OpponentType, Rarity


class Item(BaseModel):
    id: str
    name: str
    type: ItemType
    rarity: Rarity
    slot: str  # z.B. "weapon", "armor", "ring"
    description: str | None = None
    value: int = 0
    effects: list[str] | None = None

class Opponent(BaseModel):
    id: str
    name: str
    type: OpponentType
    level: int
    hp: int
    attack: int
    defense: int
    element: Element = Element.PHYSICAL
    loot_table: list[str] | None = None
    description: str | None = None
