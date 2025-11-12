"""
Test: Explorer-Agent sammelt Ressourcen auf 5x5-Karte schneller als Zufall
"""
from rpg_project.src.rl.environment import RpgEnv
import numpy as np

class RandomAgent:
    def __init__(self, env):
        self.env = env
    def act(self, obs):
        return self.env.action_space.sample()
    def run(self):
        obs, info = self.env.reset()
        done = False
        steps = 0
        collected = 0
        while not done and steps < self.env.max_steps:
            action = self.act(obs)
            obs, reward, done, _, info = self.env.step(action)
            if reward > 0:
                collected += 1
            steps += 1
        return collected, steps, info

class ExplorerAgent:
    def __init__(self, env):
        self.env = env
    def act(self, obs):
        x, y = obs
        targets = [res for res in self.env.resources if res not in self.env.collected]
        if not targets:
            return 0  # bleibe stehen
        rx, ry = targets[0]
        if (x, y) == (rx, ry):
            targets = [res for res in self.env.resources if res not in self.env.collected]
            if not targets:
                return 0
            rx, ry = targets[0]
        if x < rx:
            return 3  # rechts
        elif x > rx:
            return 2  # links
        elif y < ry:
            return 1  # runter
        elif y > ry:
            return 0  # hoch
        return 0
    def run(self):
        obs, info = self.env.reset()
        done = False
        steps = 0
        collected = 0
        while not done and steps < self.env.max_steps:
            action = self.act(obs)
            obs, reward, done, _, info = self.env.step(action)
            if reward > 0:
                collected += 1
            steps += 1
        return collected, steps, info

def test_explorer_vs_random():
    env = RpgEnv()
    explorer = ExplorerAgent(env)
    random_agent = RandomAgent(env)
    # Explorer sollte alle Ressourcen in <= 25 Schritten schaffen
    collected_e, steps_e, info_e = explorer.run()
    assert collected_e == 3
    assert steps_e <= 25
    assert info_e.get("success", False)
    # Random-Agent braucht im Schnitt mehr Schritte
    results = [random_agent.run()[1] for _ in range(10)]
    assert sum(results)/len(results) > steps_e
