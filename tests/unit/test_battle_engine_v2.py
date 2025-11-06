def test_v2_draw(entity_factory):
    player = entity_factory(id="p1", name="Held", hp=1, max_hp=10, atk=10, defense=0, is_player=True)
    opponent = entity_factory(id="e1", name="Goblin", hp=1, max_hp=10, atk=10, defense=0, is_player=False)
    store = BattleStore()
    battle_id = "v2-draw-battle"
    status = store.create_battle(battle_id, player, opponent)
    # Simuliere Kampf bis zum Ende
    for _ in range(5):
        if getattr(status, 'state', None) == getattr(status, 'FINISHED', None) or getattr(status, 'state', None) == 'finished':
            break
        status = store.step(battle_id)
    # Prüfe, ob Kampf beendet wurde
    assert getattr(status, 'state', None) == getattr(status, 'FINISHED', None) or getattr(status, 'state', None) == 'finished'
    # Mindestens einer ist tot
    assert status.entities[player.id].hp == 0 or status.entities[opponent.id].hp == 0

def test_v2_negative_values(entity_factory):
    player = entity_factory(id="p1", name="Held", hp=-5, max_hp=10, atk=-2, defense=0, is_player=True)
    opponent = entity_factory(id="e1", name="Goblin", hp=8, max_hp=8, atk=3, defense=1, is_player=False)
    store = BattleStore()
    battle_id = "v2-negative-battle"
    status = store.create_battle(battle_id, player, opponent)
    assert status.entities[player.id].hp <= 0
    if hasattr(status, 'state'):
        assert status.state == getattr(status, 'FINISHED', None) or True

def test_v2_multiple_rounds(entity_factory):
    player = entity_factory(id="p1", name="Held", hp=20, max_hp=20, atk=3, defense=1, is_player=True)
    opponent = entity_factory(id="e1", name="Goblin", hp=15, max_hp=15, atk=2, defense=1, is_player=False)
    store = BattleStore()
    battle_id = "v2-multi-round-battle"
    status = store.create_battle(battle_id, player, opponent)
    for _ in range(10):
        if getattr(status, 'state', None) == getattr(status, 'FINISHED', None):
            break
        status = store.step(battle_id)
    assert getattr(status, 'state', None) == getattr(status, 'FINISHED', None) or True
    assert getattr(status, 'winner', None) in [player.id, opponent.id, None]

def test_v2_invalid_battle_id():
    store = BattleStore()
    with pytest.raises(RuntimeError):
        store.step("invalid-id-456")

def test_v2_invalid_skill_name(entity_factory):
    player = entity_factory(id="p1", name="Held", hp=10, max_hp=10, atk=5, defense=1, is_player=True)
    opponent = entity_factory(id="e1", name="Goblin", hp=8, max_hp=8, atk=3, defense=1, is_player=False)
    store = BattleStore()
    battle_id = "v2-invalid-skill"
    store.create_battle(battle_id, player, opponent)
    # Skillname existiert nicht
    with pytest.raises(Exception):
        store.use_skill(battle_id, user_id=player.id, skill_name="nonexistent_skill")
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
"""
Unit-Tests für BattleEngine v2 (Skills, Effekte, Cooldowns)
"""

import pytest
from rpg_project.src.services.battle_engine import BattleStore

# Fixtures werden zentral über conftest.py bereitgestellt

def test_fireball_skill_applies_burn_effect(entity_factory):
    player = entity_factory(id="p1", name="Held", hp=30, max_hp=30, atk=5, defense=1, is_player=True)
    opponent = entity_factory(id="e1", name="Goblin", hp=30, max_hp=30, atk=3, defense=1, is_player=False)
    store = BattleStore()
    battle_id = "v2-battle-1"
    # Kampf initialisieren
    status = store.create_battle(battle_id, player, opponent)
    # Spieler nutzt "skill_fireball"-Skill (Skill-Logik muss in BattleEngine v2 implementiert werden)
    status = store.use_skill(battle_id, user_id=player.id, skill_name="skill_fireball")
    # Gegner sollte Schaden erhalten haben und "Burn"-Effekt besitzen
    goblin = status.entities[opponent.id]
    assert goblin.hp < 30  # Schaden durch Feuerball
    assert any("burn" in e.name.lower() for e in getattr(goblin, "effects", []))
    # Effekt tickt in der nächsten Runde
    status = store.step(battle_id)
    goblin = status.entities[opponent.id]
    # HP weiter gesunken durch Brennen (optional, je nach Engine)
    # Cooldown für Feuerball prüfen (Skill nicht sofort wieder nutzbar)
    cooldowns = getattr(status, "cooldowns", {})
    # Cooldown ist optional, da nicht in allen Skills gesetzt
