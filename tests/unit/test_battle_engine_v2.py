"""
Unit-Tests für BattleEngine v2 (Skills, Effekte, Cooldowns)
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import pytest
from rpg_project.src.services.battle_engine import BattleStore, EntityState, BattleState
from rpg_project.src.models.effects import Effect

@pytest.fixture
def store():
    return BattleStore()

@pytest.fixture
def player():
    # Spieler mit Skillpunkte-Attribut und Skills
    return EntityState(id="p1", name="Held", hp=40, max_hp=40, atk=10, defense=2, is_player=True)

@pytest.fixture
def opponent():
    return EntityState(id="e1", name="Goblin", hp=30, max_hp=30, atk=5, defense=1, is_player=False)

def test_fireball_skill_applies_burn_effect(store, player, opponent):
    battle_id = "v2-battle-1"
    # Kampf initialisieren
    status = store.create_battle(battle_id, player, opponent)
    # Spieler nutzt "Feuerball"-Skill (Skill-Logik muss in BattleEngine v2 implementiert werden)
    # Simuliere Skill-Nutzung: store.use_skill(battle_id, user_id=player.id, skill_name="fireball")
    status = store.use_skill(battle_id, user_id=player.id, skill_name="fireball")
    # Gegner sollte Schaden erhalten haben und "Brennen"-Effekt besitzen
    goblin = status.entities[opponent.id]
    assert goblin.hp < 30  # Schaden durch Feuerball
    assert any(e.name == "Brennen" for e in getattr(goblin, "effects", []))
    # Effekt tickt in der nächsten Runde
    status = store.step(battle_id)
    goblin = status.entities[opponent.id]
    # HP weiter gesunken durch Brennen
    assert goblin.hp < 30
    # Cooldown für Feuerball prüfen (Skill nicht sofort wieder nutzbar)
    cooldowns = getattr(status, "cooldowns", {})
    assert cooldowns.get(player.id, {}).get("fireball", 0) > 0
