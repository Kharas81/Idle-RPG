import pytest
from rpg_project.src.services.dialogue_manager import DialogueManager
from rpg_project.src.models.dialogue import DialogueNode

@pytest.fixture
def manager():
    # Nutzt die echte Config (guard.json5)
    return DialogueManager(config_dir="config/dialogues")

def test_start_dialogue(manager):
    node = manager.start_dialogue("guard")
    assert isinstance(node, DialogueNode)
    assert node.npc_text.startswith("Halt!")
    assert any(opt.id == "ask_quest" for opt in node.options)

def test_quest_acceptance(manager):
    # Simuliere Dialog: Start -> Quest-Angebot -> Annehmen
    node = manager.start_dialogue("guard")
    assert node.id == "start"
    node = manager.choose_option("guard", node.id, "ask_quest")
    assert node.id == "quest_offer"
    node = manager.choose_option("guard", node.id, "accept_quest")
    assert node.id == "accepted"
    # Optionale Prüfung: quest_id ist "bandit_quest"
    quest_option = [opt for opt in node.options if opt.id == "end"]
    assert quest_option

def test_dialogue_end(manager):
    node = manager.start_dialogue("guard")
    node = manager.choose_option("guard", node.id, "just_passing")
    assert node.id == "end"
    # Keine weiteren Optionen
    assert node.options == []
