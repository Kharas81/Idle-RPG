"""Unit-Tests für BattleEngine (rundenbasierter Kampf)
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import pytest

from rpg_project.src.services.battle_engine import BattleState, BattleStore, EntityState


@pytest.fixture
def store():
    return BattleStore()

@pytest.fixture
def player():
    return EntityState(id="p1", name="Held", hp=10, max_hp=10, atk=5, defense=2, is_player=True)

@pytest.fixture
def opponent():
    return EntityState(id="e1", name="Goblin", hp=8, max_hp=8, atk=3, defense=1, is_player=False)

def test_battle_start(store, player, opponent):
    battle_id = "unit-battle-1"
    status = store.create_battle(battle_id, player, opponent)
    assert status.state == BattleState.IN_PROGRESS
    assert status.turn == 1
    assert status.attacker == player.id
    assert status.defender == opponent.id
    assert status.entities[player.id].hp == 10
    assert status.entities[opponent.id].hp == 8

def test_battle_step_damage_and_turn(store, player, opponent):
    battle_id = "unit-battle-2"
    store.create_battle(battle_id, player, opponent)
    status = store.step(battle_id)
    # Spieler greift an: 5-1=4 Schaden, Goblin hat 4 HP
    assert status.entities[opponent.id].hp == 4
    assert status.turn == 2
    assert status.attacker == opponent.id
    assert status.defender == player.id

def test_battle_step_victory(store, player, opponent):
    battle_id = "unit-battle-3"
    opponent.hp = 1
    store.create_battle(battle_id, player, opponent)
    status = store.step(battle_id)
    assert status.state == BattleState.FINISHED
    assert status.winner == player.id
    assert status.entities[opponent.id].hp == 0

def test_battle_step_no_active_battle(store):
    with pytest.raises(RuntimeError):
        store.step("not-exist")
