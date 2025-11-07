from pydantic import BaseModel
from typing import Literal, Optional

class AutomationRule(BaseModel):
    trigger: Literal["hp_below"]
    threshold: int  # z.B. 30 für 30%
    action: Literal["use_heal_potion"]
    enabled: bool = True

class AutomationRuleSet(BaseModel):
    character_id: str
    rules: list[AutomationRule]
