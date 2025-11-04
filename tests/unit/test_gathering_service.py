import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import pytest
from rpg_project.src.services.gathering_service import GatheringService
from rpg_project.src.models.resource import Resource

class DummyPlayer:
    def __init__(self):
        self.inventory = []

@pytest.fixture
def world_map():
    return {
        "tiles": {
            "(2,2)": {"type": "rock", "resource": {"name": "Eisenerz", "type": "mineral", "amount": 1}},
            "(3,3)": {"type": "tree", "resource": {"name": "Holz", "type": "wood", "amount": 2}}
        }
    }

def test_gather_iron_ore(world_map):
    player = DummyPlayer()
    service = GatheringService(world_map)
    res = service.gather(player, (2,2))
    assert res is not None
    assert res.name == "Eisenerz"
    assert player.inventory[0]["name"] == "Eisenerz"
    # Ressource ist entfernt
    assert "resource" not in world_map["tiles"]["(2,2)"]

def test_gather_nothing(world_map):
    player = DummyPlayer()
    service = GatheringService(world_map)
    res = service.gather(player, (1,1))
    assert res is None
    assert player.inventory == []
