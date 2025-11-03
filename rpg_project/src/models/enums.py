from enum import Enum

class ItemType(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    CONSUMABLE = "consumable"
    QUEST = "quest"
    RESOURCE = "resource"

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
