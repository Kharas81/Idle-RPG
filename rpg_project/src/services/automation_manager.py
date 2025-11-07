from typing import Dict, List, Optional
from rpg_project.src.models.automation import AutomationRule, AutomationRuleSet

class AutomationManager:
    def __init__(self):
        self._rules: Dict[str, AutomationRuleSet] = {}

    def set_rules(self, character_id: str, rules: List[AutomationRule]):
        self._rules[character_id] = AutomationRuleSet(character_id=character_id, rules=rules)

    def get_rules(self, character_id: str) -> AutomationRuleSet:
        return self._rules.get(character_id, AutomationRuleSet(character_id=character_id, rules=[]))

    def check_and_apply(self, character_id: str, state: dict) -> Optional[str]:
        # Gibt die Aktion zurück, die automatisch ausgeführt werden soll, oder None
        ruleset = self.get_rules(character_id)
        for rule in ruleset.rules:
            if rule.enabled and rule.trigger == "hp_below":
                hp = state.get("hp", 100)
                max_hp = state.get("max_hp", 100)
                if max_hp > 0 and hp / max_hp * 100 < rule.threshold:
                    if rule.action == "use_heal_potion":
                        return "use_heal_potion"
        return None
