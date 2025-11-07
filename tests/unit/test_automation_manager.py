import pytest
from rpg_project.src.services.automation_manager import AutomationManager
from rpg_project.src.models.automation import AutomationRule

def test_set_and_get_rules():
    mgr = AutomationManager()
    rules = [AutomationRule(trigger="hp_below", threshold=30, action="use_heal_potion")]
    mgr.set_rules("hero1", rules)
    ruleset = mgr.get_rules("hero1")
    assert len(ruleset.rules) == 1
    assert ruleset.rules[0].trigger == "hp_below"
    assert ruleset.rules[0].threshold == 30
    assert ruleset.rules[0].action == "use_heal_potion"

def test_check_and_apply():
    mgr = AutomationManager()
    rules = [AutomationRule(trigger="hp_below", threshold=50, action="use_heal_potion")]
    mgr.set_rules("hero2", rules)
    # HP unter Schwelle
    state = {"hp": 20, "max_hp": 100}
    action = mgr.check_and_apply("hero2", state)
    assert action == "use_heal_potion"
    # HP über Schwelle
    state = {"hp": 80, "max_hp": 100}
    action = mgr.check_and_apply("hero2", state)
    assert action is None
