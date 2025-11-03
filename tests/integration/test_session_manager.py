import unittest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from rpg_project.src.api.session import router, create_app, world_state as api_world_state
from rpg_project.src.services.session_manager import SessionManager
from rpg_project.src.services.world_state import WorldState
from rpg_project.src.models.ecs import PositionComponent

class TestSessionManagerIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.world_state = WorldState()
        cls.app = create_app(cls.world_state)
        cls.client = TestClient(cls.app)
        cls.session_manager = SessionManager()

        # Patch API's world_state with test's instance
        api_world_state.entity_manager = cls.world_state.entity_manager

    @classmethod
    def tearDownClass(cls):
        # Close database connection after tests
        cls.session_manager.close()

    def setUp(self):
        # Reset database before each test
        self.session_manager.init_database()
        # Clear database tables before each test
        cursor = self.session_manager.connection.cursor()
        cursor.execute('DELETE FROM components_position')
        self.session_manager.connection.commit()

    def test_create_new_session(self):
        response = self.client.post("/session/new")
        self.assertEqual(response.status_code, 200)
        self.assertIn("New session created successfully.", response.json()["message"])

    def test_save_and_load_session(self):
        # Create a new session
        self.client.post("/session/new")

        # Modify world state
        entity_id = self.world_state.entity_manager.create_entity()
        self.world_state.entity_manager.add_component(entity_id, PositionComponent(5, 5))

        # Save session
        response = self.client.post("/session/save")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Session saved successfully.", response.json()["message"])

        # Modify world state again
        self.world_state.entity_manager.add_component(entity_id, PositionComponent(10, 10))

        # Load session
        response = self.client.get("/session/load")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Session loaded successfully.", response.json()["message"])

        # Verify loaded state
        position = self.world_state.entity_manager.get_component(entity_id, PositionComponent)
        self.assertEqual(position.x, 5)
        self.assertEqual(position.y, 5)

    def test_save_and_load_session_with_fixed_data(self):
        # Insert fixed data into the database
        self.session_manager.init_database()
        cursor = self.session_manager.connection.cursor()
        cursor.execute('INSERT INTO components_position (e_id, x, y) VALUES (1, 5, 5)')
        self.session_manager.connection.commit()

        # Load the session
        self.session_manager.load_game(self.world_state)

        # Validate the loaded data
        position = self.world_state.entity_manager.get_component(1, PositionComponent)
        self.assertIsNotNone(position, "PositionComponent should not be None")
        self.assertEqual(position.x, 5)
        self.assertEqual(position.y, 5)

if __name__ == "__main__":
    unittest.main()