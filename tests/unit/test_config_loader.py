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
    # GDD 2: Es sind jetzt alle Items aus der Datenbank enthalten
    assert len(items) >= 100
    ids = [item.id for item in items]
    names = [item.name for item in items]
    # Prüfe exemplarisch einige GDD-Items
    assert "potion_heal_small" in ids
    assert "Kleiner Heiltrank" in names
    assert "bomb_iron" in ids
    assert "Eisenbombe" in names
    assert "scroll_teleport_town" in ids
    assert "Schriftrolle: Stadtrückkehr" in names
    types = [item.type.value for item in items]
    assert "consumable" in types

def test_load_opponents():
    opponents = ConfigLoader.load_config("config/opponents.json5", Opponent)
    # Prüfe die neue Gegneranzahl (laut GDD: 49 Einträge)
    assert len(opponents) >= 49
    ids = [o.id for o in opponents]
    # Prüfe exemplarisch einige Gegner
    assert "goblin_scout" in ids
    goblin = next(o for o in opponents if o.id == "goblin_scout")
    assert goblin.name == "Goblin Späher"
    assert goblin.stats["atk"] == 8
    assert goblin.stats["spd"] == 12
    assert "quick_strike" in goblin.skills
    assert "basic_attack" in goblin.skills
    assert goblin.ai_policy == "Coward"
    # Prüfe einen Gegner mit mehreren Archetypen
    assert "orc_shaman" in ids
    orc_shaman = next(o for o in opponents if o.id == "orc_shaman")
    assert orc_shaman.name == "Ork-Schamane"
    assert "role_magic_fire" in orc_shaman.archetypes
    assert orc_shaman.stats["mana"] == 50
    assert "skill_heal_light" in orc_shaman.skills
