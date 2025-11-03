import gymnasium as gym
from gymnasium import spaces
import numpy as np
from rpg_project.src.services.session_manager import SessionManager
from rpg_project.src.services.world_state import WorldState
from rpg_project.src.models.ecs import EntityManager, PositionComponent, HPComponent, ActionRequestComponent

class RpgEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.session_manager = SessionManager()
        self.world_state = WorldState()
        self.entity_manager = self.world_state.entity_manager
        self.player_e_id = None

        # Define observation and action spaces
        self.observation_space = spaces.Dict({
            "position": spaces.Box(low=0, high=100, shape=(2,), dtype=np.int32),
            "hp": spaces.Box(low=0, high=100, shape=(1,), dtype=np.int32)
        })
        self.action_space = spaces.Discrete(10)  # Example: 10 possible actions

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.session_manager.init_database()
        self.session_manager.new_game()
        self.player_e_id = self.entity_manager.create_entity()
        self.entity_manager.add_component(self.player_e_id, PositionComponent(0, 0))
        self.entity_manager.add_component(self.player_e_id, HPComponent(100))
        return self._get_observation(), {}

    def step(self, action):
        # Translate action into game logic
        self.entity_manager.add_component(self.player_e_id, ActionRequestComponent(action))
        self.world_state.tick()

        obs = self._get_observation()
        reward = self._calculate_reward()
        terminated = self._is_terminated()
        truncated = False
        return obs, reward, terminated, truncated, {}

    def _get_observation(self):
        position = self.entity_manager.get_component(self.player_e_id, PositionComponent)
        hp = self.entity_manager.get_component(self.player_e_id, HPComponent)
        if position is None or hp is None:
            raise ValueError("Player entity is missing required components: PositionComponent or HPComponent")
        return {
            "position": np.array([position.x, position.y], dtype=np.int32),
            "hp": np.array([hp.value], dtype=np.int32)
        }

    def _calculate_reward(self):
        # Placeholder reward logic
        return 1

    def _is_terminated(self):
        # Placeholder termination logic
        return False