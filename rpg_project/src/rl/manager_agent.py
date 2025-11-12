"""
ManagerAgent: Steuert spezialisierte Agenten (Explorer, Fighter, Crafter) und erfüllt strategische Ziele
"""
from rpg_project.src.rl.environment import RpgEnv
from scripts.train_explorer import ExplorerAgent
from scripts.train_fighter import FighterAgent
# CrafterAgent wäre analog zu implementieren

class ManagerAgent:
    def __init__(self, env: RpgEnv):
        self.env = env
        self.explorer = ExplorerAgent(env)
        self.fighter = FighterAgent(env)
        # self.crafter = CrafterAgent(env)  # Platzhalter
        self.log = []

    def achieve_goal(self, goal: str = "craft_item", item: str = "Eisenschwert", required_resources: int = 3):
        """
        Erfüllt das Ziel, z.B. ein Item craften:
        1. Ressourcen sammeln (Explorer)
        2. Gegner besiegen (Fighter, falls nötig)
        3. Item craften (Crafter)
        """
        self.log.append(f"Starte Ziel: {goal} für {item}")
        # Schritt 1: Ressourcen sammeln
        collected, steps, info = self.explorer.run()
        self.log.append(f"Explorer sammelt Ressourcen: {collected}")
        # Schritt 2: Gegner besiegen (optional)
        # result = self.fighter.run()
        # self.log.append(f"Fighter besiegt Gegner: {result}")
        # Schritt 3: Item craften (simuliert)
        crafted = False
        if collected >= required_resources:
            crafted = True
            self.log.append(f"Crafter stellt {item} her!")
        else:
            self.log.append(f"Nicht genug Ressourcen für {item}! Benötigt: {required_resources}, gesammelt: {collected}")
        return crafted, self.log
