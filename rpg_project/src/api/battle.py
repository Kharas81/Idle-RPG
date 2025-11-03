from flask import Blueprint, request, jsonify
from rpg_project.src.services.battle_engine import BattleEngine
from rpg_project.src.models.ecs import EntityManager, ActionRequestComponent

battle_api = Blueprint('battle_api', __name__)
battle_engine = BattleEngine()

# Mock world_state for testing purposes
class MockWorldState:
    def __init__(self):
        self.entity_manager = EntityManager()

    def add_component(self, entity_id, component):
        self.entity_manager.add_component(entity_id, component)

    def remove_component(self, entity_id, component_type):
        self.entity_manager.remove_component(entity_id, component_type)

world_state = MockWorldState()

# Debugging: Log entity creation
def log_entity_creation(entity_id):
    print(f"Ensuring entities exist: {entity_id}")
    try:
        world_state.entity_manager.create_entity(entity_id)
        print(f"Entity {entity_id} created successfully.")
    except ValueError as e:
        print(f"Entity {entity_id} already exists: {e}")

# Debugging: Log entity manager state
def log_entity_manager_state():
    print(f"EntityManager state before adding component: {world_state.entity_manager._entities}")

@battle_api.route('/battle/start', methods=['POST'])
def start_battle():
    data = request.get_json()
    if not data or 'battle_id' not in data or 'entities' not in data:
        return jsonify({"error": "Invalid request data"}), 400

    battle_id = data['battle_id']
    entities = data['entities']
    # Debugging: Log entity creation
    for entity_id in entities:
        log_entity_creation(entity_id)
        log_entity_manager_state()

    battle_engine.start_battle(battle_id, entities)
    return jsonify({"message": "Battle started", "battle_id": battle_id})

@battle_api.route('/battle/<battle_id>/state', methods=['GET'])
def get_battle_state(battle_id):
    battle = battle_engine.battles.get(battle_id)
    if not battle:
        return jsonify({"error": "Battle not found"}), 404
    return jsonify({"battle_id": battle_id, "state": battle.battle_state})

@battle_api.route('/battle/<battle_id>/step', methods=['POST'])
def process_battle_step(battle_id):
    data = request.get_json()
    if not data or 'entity_id' not in data or 'action' not in data:
        return jsonify({"error": "Invalid request data"}), 400

    entity_id = data['entity_id']
    action = data['action']
    # Set ActionRequestComponent for the entity in the world state
    world_state.add_component(entity_id, ActionRequestComponent(action))
    return jsonify({"message": "Action processed", "battle_id": battle_id})