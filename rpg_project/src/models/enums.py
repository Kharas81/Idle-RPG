from enum import Enum
class EventType(str, Enum):
    ON_ENEMY_DEFEATED = "ON_ENEMY_DEFEATED"
from enum import Enum


class ItemType(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    CONSUMABLE = "consumable"
    QUEST = "quest"
    RESOURCE = "resource"
    ACCESSORY = "accessory"
    TRADE_GOOD = "trade_good"

# Equipment-Slots für Ausrüstungssystem
class EquipmentSlot(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"

class Rarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

class OpponentType(Enum):
    BEAST = "beast"
    HUMANOID = "humanoid"
    UNDEAD = "undead"
    BOSS = "boss"

class Element(Enum):
    PHYSICAL = "physical"
    FIRE = "fire"
    WATER = "water"
    EARTH = "earth"
    AIR = "air"
    LIGHT = "light"
    DARK = "dark"
