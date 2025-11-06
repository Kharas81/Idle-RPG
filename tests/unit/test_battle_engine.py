def test_battle_draw(entity_factory):
    # Beide haben gleich viel HP und töten sich gegenseitig
    player = entity_factory(id="p1", name="held", hp=1, max_hp=10, atk=10, defense=0, is_player=True)
    opponent = entity_factory(id="e1", name="Goblin", hp=1, max_hp=10, atk=10, defense=0, is_player=False)
    store = BattleStore()
    battle_id = "draw-battle"
    status = store.create_battle(battle_id, player, opponent)
    # Simuliere Kampf bis zum Ende
    for _ in range(5):
        if status.state == BattleState.FINISHED:
            break
        status = store.step(battle_id)
    # Prüfe, ob Kampf beendet wurde
    assert status.state == BattleState.FINISHED
    # Mindestens einer ist tot
    assert status.entities[player.id].hp == 0 or status.entities[opponent.id].hp == 0

def test_battle_negative_values(entity_factory):
    # Negative Werte für HP und ATK sollten abgefangen werden
    player = entity_factory(id="p1", name="held", hp=-5, max_hp=10, atk=-2, defense=0, is_player=True)
    opponent = entity_factory(id="e1", name="Goblin", hp=8, max_hp=8, atk=3, defense=1, is_player=False)
    store = BattleStore()
    battle_id = "negative-battle"
    status = store.create_battle(battle_id, player, opponent)
    # Spieler sollte sofort tot sein oder ignoriert werden
    assert status.entities[player.id].hp <= 0
    # Prüfe, ob Kampf nach spätestens 1 Runde beendet ist
    for _ in range(2):
        if status.state == BattleState.FINISHED:
            break
        status = store.step(battle_id)
    assert status.state == BattleState.FINISHED

def test_battle_multiple_rounds(entity_factory):
    # Mehrere Runden Kampf
    player = entity_factory(id="p1", name="held", hp=20, max_hp=20, atk=3, defense=1, is_player=True)
    opponent = entity_factory(id="e1", name="Goblin", hp=15, max_hp=15, atk=2, defense=1, is_player=False)
    store = BattleStore()
    battle_id = "multi-round-battle"
    status = store.create_battle(battle_id, player, opponent)
    for _ in range(20):
        if status.state == BattleState.FINISHED:
            break
        status = store.step(battle_id)
    # Am Ende sollte einer gewonnen haben
    assert status.state == BattleState.FINISHED
    assert status.winner in [player.id, opponent.id]

def test_battle_invalid_battle_id(entity_factory):
    # Schritt mit ungültiger Battle-ID
    store = BattleStore()
    with pytest.raises(RuntimeError):
        store.step("invalid-id-123")
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
"""
Unit-Tests für BattleEngine (rundenbasierter Kampf)
"""

import pytest
from rpg_project.src.services.battle_engine import BattleState, BattleStore

# Fixtures werden zentral über conftest.py bereitgestellt

def test_battle_start(entity_factory):
    player = entity_factory(id="p1", name="Held", hp=10, max_hp=10, atk=5, defense=1, is_player=True)
    opponent = entity_factory(id="e1", name="Goblin", hp=8, max_hp=8, atk=3, defense=1, is_player=False)
    store = BattleStore()
    battle_id = "unit-battle-1"
    status = store.create_battle(battle_id, player, opponent)
    assert status.state == BattleState.IN_PROGRESS
    assert status.turn == 1
    assert status.attacker == player.id
    assert status.defender == opponent.id
    assert status.entities[player.id].hp == 10
    assert status.entities[opponent.id].hp == 8

def test_battle_step_damage_and_turn(entity_factory):
    player = entity_factory(id="p1", name="Held", hp=10, max_hp=10, atk=5, defense=1, is_player=True)
    opponent = entity_factory(id="e1", name="Goblin", hp=8, max_hp=8, atk=3, defense=1, is_player=False)
    store = BattleStore()
    battle_id = "unit-battle-2"
    store.create_battle(battle_id, player, opponent)
    status = store.step(battle_id)
    # Spieler greift an: 5-1=4 Schaden, Goblin hat 4 HP
    assert status.entities[opponent.id].hp == 4
    assert status.turn == 2
    assert status.attacker == opponent.id
    assert status.defender == player.id

def test_battle_step_victory(entity_factory):
    player = entity_factory(id="p1", name="Held", hp=10, max_hp=10, atk=5, defense=1, is_player=True)
    opponent = entity_factory(id="e1", name="Goblin", hp=1, max_hp=8, atk=3, defense=1, is_player=False)
    store = BattleStore()
    battle_id = "unit-battle-3"
    store.create_battle(battle_id, player, opponent)
    status = store.step(battle_id)
    assert status.state == BattleState.FINISHED
    assert status.winner == player.id
    assert status.entities[opponent.id].hp == 0

def test_battle_step_no_active_battle():
    store = BattleStore()
    with pytest.raises(RuntimeError):
        store.step("not-exist")
