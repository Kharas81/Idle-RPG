import sqlite3
from pathlib import Path
from rpg_project.src.services.world_state import WorldState
from rpg_project.src.models.ecs import PositionComponent

DB_PATH = './saves/game.db'

class SessionManager:
    def __init__(self):
        self.db_path = Path(DB_PATH)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = None

    def init_database(self):
        self.connection = sqlite3.connect(self.db_path)
        cursor = self.connection.cursor()

        # Create tables for components
        cursor.execute('''CREATE TABLE IF NOT EXISTS components_position (
            e_id INTEGER PRIMARY KEY,
            x INTEGER,
            y INTEGER
        )''')

        # Create meta table for versioning
        cursor.execute('''CREATE TABLE IF NOT EXISTS meta (
            key TEXT PRIMARY KEY,
            value TEXT
        )''')
        cursor.execute('''INSERT OR IGNORE INTO meta (key, value) VALUES ('version', '1')''')

        self.connection.commit()

    def check_version(self):
        if self.connection is None:
            self.init_database()
        cursor = self.connection.cursor()
        cursor.execute('SELECT value FROM meta WHERE key = "version"')
        version = cursor.fetchone()
        if version is None or version[0] != '1':
            raise ValueError("Database version mismatch or missing meta table.")

    def save_position_components(self, world_state: WorldState):
        if self.connection is None:
            self.init_database()
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM components_position')

        entities = world_state.entity_manager.get_entities_with(PositionComponent)
        for e_id, components in entities.items():
            position = components[PositionComponent]
            cursor.execute('INSERT INTO components_position (e_id, x, y) VALUES (?, ?, ?)',
                           (e_id, position.x, position.y))

        self.connection.commit()

    def load_position_components(self, world_state: WorldState):
        if self.connection is None:
            self.init_database()
        cursor = self.connection.cursor()
        cursor.execute('SELECT e_id, x, y FROM components_position')
        for e_id, x, y in cursor.fetchall():
            if e_id not in world_state.entity_manager._entities:
                world_state.entity_manager._entities.add(e_id)
                world_state.entity_manager._components[e_id] = {}
            world_state.entity_manager.add_component(e_id, PositionComponent(x, y))

    def save_game(self, world_state: WorldState):
        self.save_position_components(world_state)

    def load_game(self, world_state: WorldState):
        self.load_position_components(world_state)

    def close(self):
        if self.connection:
            self.connection.close()

    def new_game(self):
        self.init_database()
        self.connection.execute('DELETE FROM components_position')
        self.connection.commit()