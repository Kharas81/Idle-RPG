
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
    # Neue Felder für Archetypen-System
    archetypes: list[str] | None = None
    stats: dict[str, int] = {}
    skills: list[str] = []
    ai_policy: str | None = None
    xp: int | None = None
    # Alte Felder bleiben optional für Kompatibilität
    type: OpponentType | None = None
    level: int | None = None
    hp: int | None = None
    attack: int | None = None
    defense: int | None = None
    element: Element = Element.PHYSICAL
    loot_table: list[str] | None = None
    description: str | None = None
