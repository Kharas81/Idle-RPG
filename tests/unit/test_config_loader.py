def test_merge_skills_multiple_archetypes():
    # Gegner mit mehreren Archetypen
    from rpg_project.src.services.config_loader import merge_skills
    arch_skills = ["basic_attack", "skill_arrow_shot"]
    opp_skills = ["quick_strike"]
    result = merge_skills(arch_skills, opp_skills)
    assert result == ["basic_attack", "skill_arrow_shot", "quick_strike"]

def test_merge_skills_overwrite():
    # Gegner mit skills_overwrite: true
    from rpg_project.src.services.config_loader import merge_skills
    arch_skills = ["basic_attack", "skill_arrow_shot"]
    opp_skills = ["quick_strike"]
    result = merge_skills(arch_skills, opp_skills, overwrite=True)
    assert result == ["quick_strike"]

def test_merge_skills_no_opponent_skills():
    # Gegner ohne eigene Skills
    from rpg_project.src.services.config_loader import merge_skills
    arch_skills = ["basic_attack"]
    opp_skills = []
    result = merge_skills(arch_skills, opp_skills)
    assert result == ["basic_attack"]

def test_merge_skills_empty_archetype():
    # Archetyp ohne Skills
    from rpg_project.src.services.config_loader import merge_skills
    arch_skills = []
    opp_skills = ["quick_strike"]
    result = merge_skills(arch_skills, opp_skills)
    assert result == ["quick_strike"]

def test_merge_skills_duplicates():
    # Duplikate werden entfernt
    from rpg_project.src.services.config_loader import merge_skills
    arch_skills = ["basic_attack", "quick_strike"]
    opp_skills = ["quick_strike", "basic_attack"]
    result = merge_skills(arch_skills, opp_skills)
    assert result == ["basic_attack", "quick_strike"]
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from rpg_project.src.models.core import Item, Opponent
from rpg_project.src.services.config_loader import ConfigLoader


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
    assert len(opponents) == 6
    goblin = opponents[0]
    assert goblin.id == "goblin_scout"
    assert goblin.name == "Goblin Späher"
    assert goblin.stats["atk"] == 8
    assert goblin.stats["spd"] == 12
    assert "quick_strike" in goblin.skills
    assert "basic_attack" in goblin.skills
    assert goblin.ai_policy == "Coward"
