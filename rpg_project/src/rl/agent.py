"""
RL-Agent für das Idle-RPG: trainiert, kämpft und speichert Modelle
"""
import numpy as np
import gymnasium as gym
from rpg_project.src.rl.environment import RpgEnv

class FighterAgent:
    """
    Ein einfacher RL-Agent, der zufällig Aktionen wählt (Dummy für End-to-End-Test)
    """
    def __init__(self, env: gym.Env):
        self.env = env
        self.model = None  # Platzhalter für ein echtes Modell

    def train(self, episodes=10):
        # Dummy-Training: Zufällige Aktionen
        for ep in range(episodes):
            obs, info = self.env.reset()
            done = False
            while not done:
                action = self.env.action_space.sample()
                obs, reward, done, _, info = self.env.step(action)
        self.model = "dummy-trained"

    def act(self, obs):
        # Dummy-Policy: Zufällige Aktion
        return self.env.action_space.sample()

    def save(self, path):
        # Speichert das Dummy-Modell
        with open(path, "w") as f:
            f.write(str(self.model))

    def load(self, path):
        # Lädt das Dummy-Modell
        with open(path, "r") as f:
            self.model = f.read()
