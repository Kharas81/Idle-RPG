import pytest
from rpg_project.src.services.dungeon_generator import DungeonGenerator
import json5

def test_dungeon_reproducibility():
    config = {"width": 8, "height": 8, "num_rooms": 4}
    gen = DungeonGenerator(config)
    d1 = gen.generate(seed=42)
    d2 = gen.generate(seed=42)
    assert d1 == d2
    assert d1["width"] == 8
    assert d1["height"] == 8
    assert len(d1["rooms"]) == 4
    # Start und Ziel sind gesetzt
    tiles = d1["tiles"]
    starts = sum(row.count(2) for row in tiles)
    ends = sum(row.count(3) for row in tiles)
    assert starts == 1
    assert ends == 1
