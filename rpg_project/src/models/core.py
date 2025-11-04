
from pydantic import BaseModel

from .enums import Element, ItemType, OpponentType, Rarity



class Item(BaseModel):
    id: str
    name: str
    type: ItemType
    rarity: Rarity | None = None
    slot: str | None = None  # z.B. "WEAPON", "ARMOR", "CONSUMABLE", "RESOURCE"
    description: str | None = None
    value_gold: int | None = None
    max_stack: int | None = None
    icon_id: str | None = None
    effect: dict | None = None  # Für Consumables
    stats_bonus: dict | None = None  # Für Equipment
    # Für Kompatibilität mit alter Struktur
    value: int | None = None
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
