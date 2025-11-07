"""
DungeonGenerator: Erzeugt prozedurale Dungeons basierend auf Seed und Regeln aus der Config.
"""
import random
from typing import List, Dict, Any
import json

class DungeonGenerator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def generate(self, seed: int) -> Dict[str, Any]:
        rnd = random.Random(seed)
        width = self.config.get("width", 10)
        height = self.config.get("height", 10)
        num_rooms = self.config.get("num_rooms", 5)
        # Dungeon als 2D-Array (0=Wand, 1=Raum, 2=Start, 3=Ziel)
        dungeon = [[0 for _ in range(width)] for _ in range(height)]
        rooms = []
        for _ in range(num_rooms):
            rx = rnd.randint(1, width-2)
            ry = rnd.randint(1, height-2)
            dungeon[ry][rx] = 1
            rooms.append((rx, ry))
        # Start- und Zielraum
        if rooms:
            start = rooms[0]
            end = rooms[-1]
            dungeon[start[1]][start[0]] = 2
            dungeon[end[1]][end[0]] = 3
        return {
            "width": width,
            "height": height,
            "tiles": dungeon,
            "rooms": rooms,
            "seed": seed
        }
