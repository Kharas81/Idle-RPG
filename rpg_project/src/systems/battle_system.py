from rpg_project.src.models.ecs import ActionRequestComponent, InBattleComponent
from rpg_project.src.services.battle_engine import BattleEngine

class BattleSystem:
    def __init__(self, battle_engine: BattleEngine):
        self.battle_engine = battle_engine

    def update(self, world_state):
        for e_id, action_request in world_state.get_entities_with(ActionRequestComponent):
            battle = self.battle_engine.get_battle_for_entity(e_id)
            if battle:
                battle.process_step(action_request.action)

                if battle.is_finished():
                    self.battle_engine.end_battle(battle.battle_id)
                    world_state.remove_component(e_id, InBattleComponent)

                world_state.remove_component(e_id, ActionRequestComponent)