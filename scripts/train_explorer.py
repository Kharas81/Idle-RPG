"""
Trainingsskript für den RL-Explorer-Agenten
"""
from rpg_project.src.rl.environment import RpgEnv
import numpy as np

class ExplorerAgent:
    """
    Dummy-Agent: Bewegt sich systematisch durch die Karte, um Ressourcen zu sammeln
    """
    def __init__(self, env):
        self.env = env

    def act(self, obs):
        # Systematisch: erst Zeile ablaufen, dann nächste
        x, y = obs
        if x < self.env.grid_size-1:
            return 3  # rechts
        elif y < self.env.grid_size-1:
            return 1  # runter
        else:
            return 0  # hoch (bleibt stehen)

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

if __name__ == "__main__":
    env = RpgEnv()
    agent = ExplorerAgent(env)
    collected, steps, info = agent.run()
    print(f"Gesammelte Ressourcen: {collected} in {steps} Schritten. Erfolg: {info.get('success', False)}")
