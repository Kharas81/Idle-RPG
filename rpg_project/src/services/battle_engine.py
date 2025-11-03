class BattleSession:
    def __init__(self, battle_id: str, entities: list):
        self.battle_id = battle_id
        self.entities = entities
        self.turn_order = []  # Define turn order logic here
        self.battle_state = "active"

    def process_step(self, action: dict):
        # Implement damage calculation and turn processing logic
        pass

    def is_finished(self):
        # Check if the battle is over
        return self.battle_state == "finished"

class BattleEngine:
    def __init__(self):
        self.battles = {}

    def start_battle(self, battle_id: str, entities: list):
        self.battles[battle_id] = BattleSession(battle_id, entities)

    def get_battle_for_entity(self, entity_id: int):
        for battle in self.battles.values():
            if entity_id in battle.entities:
                return battle
        return None

    def end_battle(self, battle_id: str):
        if battle_id in self.battles:
            del self.battles[battle_id]