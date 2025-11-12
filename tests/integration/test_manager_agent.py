"""
Integrationstest: Manager-Agent erfüllt Crafting-Ziel
"""
from rpg_project.src.rl.environment import RpgEnv
from rpg_project.src.rl.manager_agent import ManagerAgent

def test_manager_crafting_goal():
    env = RpgEnv()
    manager = ManagerAgent(env)
    # Die Karte hat 3 Ressourcenpunkte, also muss das Rezept darauf abgestimmt sein
    crafted, log = manager.achieve_goal(goal="craft_item", item="Eisenschwert", required_resources=3)
    assert crafted, "Manager-Agent sollte das Item craften können."
    assert any("Crafter stellt Eisenschwert her!" in entry for entry in log)
