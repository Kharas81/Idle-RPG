from typing import Dict, Optional
from rpg_project.src.models.dialogue import Dialogue, DialogueNode, DialogueOption
import json5
import os

class DialogueManager:
    def __init__(self, config_dir: str = "config/dialogues"):
        self.dialogues: Dict[str, Dialogue] = {}
        self.config_dir = config_dir
        self.load_all_dialogues()

    def load_all_dialogues(self):
        if not os.path.exists(self.config_dir):
            return
        for fname in os.listdir(self.config_dir):
            if fname.endswith(".json5"):
                with open(os.path.join(self.config_dir, fname), "r") as f:
                    data = json5.load(f)
                    dialogue = Dialogue(**data)
                    self.dialogues[dialogue.npc_id] = dialogue

    def start_dialogue(self, npc_id: str) -> Optional[DialogueNode]:
        dialogue = self.dialogues.get(npc_id)
        if not dialogue:
            return None
        return self.get_node(npc_id, dialogue.start_id)

    def get_node(self, npc_id: str, node_id: str) -> Optional[DialogueNode]:
        dialogue = self.dialogues.get(npc_id)
        if not dialogue:
            return None
        for node in dialogue.nodes:
            if node.id == node_id:
                return node
        return None

    def choose_option(self, npc_id: str, current_node_id: str, option_id: str) -> Optional[DialogueNode]:
        node = self.get_node(npc_id, current_node_id)
        if not node:
            return None
        for option in node.options:
            if option.id == option_id:
                if option.next_id:
                    return self.get_node(npc_id, option.next_id)
                else:
                    return None  # Dialog endet
        return None

dialogue_manager = DialogueManager()
