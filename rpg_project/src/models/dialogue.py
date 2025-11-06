from pydantic import BaseModel
from typing import List, Optional

class DialogueOption(BaseModel):
    id: str
    text: str
    next_id: Optional[str] = None
    quest_id: Optional[str] = None  # Falls diese Option eine Quest startet

class DialogueNode(BaseModel):
    id: str
    npc_text: str
    options: List[DialogueOption]

class Dialogue(BaseModel):
    npc_id: str
    nodes: List[DialogueNode]
    start_id: str
