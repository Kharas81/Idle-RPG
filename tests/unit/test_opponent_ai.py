"""
Unit-Tests für OpponentAI (Gegner-KI)
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import pytest
from rpg_project.src.services.opponent_ai import OpponentAI

class DummyState:
    def __init__(self, hp, max_hp):
        self.hp = hp
        self.max_hp = max_hp

@pytest.fixture
def coward_policy():
    return {"type": "coward", "flee_threshold": 0.2}

@pytest.fixture
def brave_policy():
    return {"type": "brave"}

def test_coward_flees_at_20_percent(coward_policy):
    ai = OpponentAI(coward_policy)
    state = DummyState(hp=2, max_hp=10)  # 20%
    action = ai.decide_action(state, None)
    assert action == "flee"

def test_coward_attacks_above_threshold(coward_policy):
    ai = OpponentAI(coward_policy)
    state = DummyState(hp=3, max_hp=10)  # 30%
    action = ai.decide_action(state, None)
    assert action == "attack"

def test_brave_always_attacks(brave_policy):
    ai = OpponentAI(brave_policy)
    state = DummyState(hp=1, max_hp=10)
    action = ai.decide_action(state, None)
    assert action == "attack"
