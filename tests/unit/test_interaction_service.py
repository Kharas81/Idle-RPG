"""Unit-Test für den InteractionService: Testet das Öffnen einer Truhe und den Erhalt des Loots.
"""
from rpg_project.src.models.character import Character
from rpg_project.src.models.interactables import Interactable, InteractableState, InteractableType
from rpg_project.src.services.event_manager import EventManager
from rpg_project.src.services.interaction_service import InteractionService


class DummyEventCollector:
    def __init__(self):
        self.events = []
    def on_event(self, data):
        self.events.append(data)

def test_open_chest_gives_loot():
    # Setup: Truhe und Charakter
    chest = Interactable(
        id="chest_1",
        type=InteractableType.CHEST,
        position=(2, 2),
        state=InteractableState.CLOSED,
        loot=["gold_coin", "healing_potion"],
        properties={"description": "Eine alte Holztruhe."}
    )
    interactables = {chest.id: chest}
    character = Character(id="hero_1", name="Held", inventory=[])
    event_manager = EventManager()
    collector = DummyEventCollector()
    event_manager.subscribe("ON_CHEST_OPENED", collector.on_event)
    service = InteractionService(event_manager, interactables)

    # Aktion: Truhe öffnen
    result = service.interact(character, "chest_1")

    # Erwartung: Erfolg, Loot im Inventar, Event ausgelöst
    assert result["success"] is True
    assert set(result["loot"]) == {"gold_coin", "healing_potion"}
    assert set(character.inventory) == {"gold_coin", "healing_potion"}
    assert chest.state == InteractableState.OPEN
    assert len(collector.events) == 1
    assert collector.events[0]["chest_id"] == "chest_1"
    assert set(collector.events[0]["loot"]) == {"gold_coin", "healing_potion"}


def test_open_chest_twice_fails():
    chest = Interactable(
        id="chest_2",
        type=InteractableType.CHEST,
        position=(1, 1),
        state=InteractableState.CLOSED,
        loot=["ruby"],
        properties={}
    )
    interactables = {chest.id: chest}
    character = Character(id="hero_2", name="Held2", inventory=[])
    event_manager = EventManager()
    service = InteractionService(event_manager, interactables)
    # Erstes Öffnen
    result1 = service.interact(character, "chest_2")
    # Zweites Öffnen
    result2 = service.interact(character, "chest_2")
    assert result1["success"] is True
    assert result2["success"] is False
    assert "already open" in result2["error"]

def test_open_locked_chest_fails():
    chest = Interactable(
        id="chest_3",
        type=InteractableType.CHEST,
        position=(0, 0),
        state=InteractableState.LOCKED,
        loot=["emerald"],
        properties={}
    )
    interactables = {chest.id: chest}
    character = Character(id="hero_3", name="Held3", inventory=[])
    event_manager = EventManager()
    service = InteractionService(event_manager, interactables)
    result = service.interact(character, "chest_3")
    assert result["success"] is False
    assert "locked" in result["error"]

def test_interact_unknown_id():
    interactables = {}
    character = Character(id="hero_4", name="Held4", inventory=[])
    event_manager = EventManager()
    service = InteractionService(event_manager, interactables)
    result = service.interact(character, "not_exist")
    assert result["success"] is False
    assert "not found" in result["error"]

