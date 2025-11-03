import unittest
from flask import Flask
from rpg_project.src.api.battle import MockWorldState, battle_engine, battle_api
from rpg_project.src.models.ecs import StatsComponent, ActionRequestComponent

class TestBattleAPI(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(battle_api)
        self.client = self.app.test_client()

        # Reset MockWorldState for each test
        global world_state
        world_state = MockWorldState()

    def test_start_battle(self):
        response = self.client.post('/battle/start', json={
            'battle_id': 'battle_1',
            'entities': [1, 2]
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Battle started', response.json['message'])

    def test_get_battle_state(self):
        self.battle_engine.start_battle('battle_1', [1, 2])
        response = self.client.get('/battle/battle_1/state')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['state'], 'active')

    def test_process_battle_step(self):
        self.battle_engine.start_battle('battle_1', [1, 2])
        response = self.client.post('/battle/battle_1/step', json={
            'entity_id': 1,
            'action': {'type': 'attack', 'target': 2}
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Action processed', response.json['message'])

if __name__ == '__main__':
    unittest.main()