"""
RpgEnv: Erweiterte RL-Umgebung für Navigation und Ressourcen
"""
RpgEnv: Erweiterte RL-Umgebung für Navigation und Ressourcen
"""
import gymnasium as gym
from gymnasium import spaces
import numpy as np

class RpgEnv(gym.Env):
    """
    RL-Umgebung für das Idle-RPG. Jetzt mit 5x5-Karte und Ressourcenpunkten.
    """
    def __init__(self, config=None):
        self.grid_size = 5
        self.action_space = spaces.Discrete(4)  # 0=hoch, 1=runter, 2=links, 3=rechts
        self.observation_space = spaces.Box(low=0, high=self.grid_size-1, shape=(2,), dtype=int)  # [x, y]
        self.state = np.array([0, 0])  # Startposition oben links
        self.resources = {(1, 1), (3, 2), (4, 4)}  # Ressourcenpunkte
        self.collected = set()
        self.max_steps = 50
        self.steps = 0
        self.config = config

    def reset(self, seed=None, options=None):
        self.state = np.array([0, 0])
        self.collected = set()
        self.steps = 0
        return self.state.copy(), {}

    def step(self, action):
        x, y = self.state
        if action == 0 and y > 0:
            y -= 1
        elif action == 1 and y < self.grid_size-1:
            y += 1
        elif action == 2 and x > 0:
            x -= 1
        elif action == 3 and x < self.grid_size-1:
            x += 1
        self.state = np.array([x, y])
        self.steps += 1
        reward = 0
        done = False
        info = {}
        if tuple(self.state) in self.resources and tuple(self.state) not in self.collected:
            self.collected.add(tuple(self.state))
            reward = 10
        if len(self.collected) == len(self.resources):
            done = True
            info["success"] = True
        if self.steps >= self.max_steps:
            done = True
        return self.state.copy(), reward, done, False, info

    def render(self):
        grid = np.full((self.grid_size, self.grid_size), ".")
        for rx, ry in self.resources:
            grid[ry, rx] = "R"
        for cx, cy in self.collected:
            grid[cy, cx] = "C"
        x, y = self.state
        grid[y, x] = "A"
        print("\n".join([" ".join(row) for row in grid]))

    def close(self):
        pass
