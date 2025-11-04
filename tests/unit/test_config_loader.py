import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from rpg_project.src.services.config_loader import ConfigLoader
from rpg_project.src.models.core import Item, Opponent


def test_load_items():
    items = ConfigLoader.load_config("config/items.json5", Item)
    assert len(items) == 3
    names = [item.name for item in items]
    types = [item.type.value for item in items]
    assert "Heiltrank" in names
    assert "Eisenschwert" in names
    assert "Lederrüstung" in names
    assert "weapon" in types
    assert "armor" in types
    assert "consumable" in types

def test_load_opponents():
    opponents = ConfigLoader.load_config("config/opponents.json5", Opponent)
    assert len(opponents) == 2
    assert opponents[0].name == "Schleim"
    assert opponents[1].element.value == "earth"
