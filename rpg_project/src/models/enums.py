from enum import Enum

class ItemType(Enum):
    CONSUMABLE = "consumable"
    EQUIPMENT = "equipment"

class OpponentType(Enum):
    BEAST = "beast"
    HUMANOID = "humanoid"