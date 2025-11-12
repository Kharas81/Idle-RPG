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
        # Nach jedem Schritt: Zielauswahl neu treffen
        x, y = obs
        targets = [res for res in self.env.resources if res not in self.env.collected]
        if not targets:
            return 0  # bleibe stehen
        # Wähle das nächste Ziel, das noch nicht gesammelt ist
        rx, ry = targets[0]
        if (x, y) == (rx, ry):
            # Ziel erreicht, im nächsten Schritt neues Ziel wählen
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
            # Nach jedem Schritt: Position und gesammelte Ressourcen prüfen
            collected = len(self.env.collected)
            steps += 1
        return collected, steps, info

if __name__ == "__main__":
    env = RpgEnv()
    agent = ExplorerAgent(env)
    collected, steps, info = agent.run()
    print(f"Gesammelte Ressourcen: {collected} in {steps} Schritten. Erfolg: {info.get('success', False)}")
