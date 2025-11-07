from fastapi import APIRouter, Body
from rpg_project.src.services.automation_manager import AutomationManager
from rpg_project.src.models.automation import AutomationRule, AutomationRuleSet

router = APIRouter()
automation_manager = AutomationManager()

@router.post("/automation/rules")
def set_automation_rules(character_id: str = Body(...), rules: list[AutomationRule] = Body(...)):
    automation_manager.set_rules(character_id, rules)
    return {"status": "ok"}

@router.get("/automation/rules")
def get_automation_rules(character_id: str):
    ruleset = automation_manager.get_rules(character_id)
    return ruleset.dict()
