"""
Trainingsskript für den Manager-Agenten
"""
from rpg_project.src.rl.environment import RpgEnv
from rpg_project.src.rl.manager_agent import ManagerAgent

def main():
    env = RpgEnv()
    manager = ManagerAgent(env)
    crafted, log = manager.achieve_goal(goal="craft_item", item="Eisenschwert")
    print("Manager-Agent Log:")
    for entry in log:
        print(entry)
    if crafted:
        print("✅ Ziel erreicht: Item wurde gecraftet!")
    else:
        print("❌ Ziel nicht erreicht: Item konnte nicht gecraftet werden.")

if __name__ == "__main__":
    main()
