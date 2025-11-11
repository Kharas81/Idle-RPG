"""
Trainingsskript für den RL-Kämpfer-Agenten
"""
from rpg_project.src.rl.environment import RpgEnv
from rpg_project.src.rl.agent import FighterAgent

if __name__ == "__main__":
    env = RpgEnv()
    agent = FighterAgent(env)
    print("Starte Training...")
    agent.train(episodes=20)
    print("Speichere Modell...")
    agent.save("fighter_agent.model")
    print("Lade Modell...")
    agent.load("fighter_agent.model")
    print("Testlauf gegen Dummy-Gegner...")
    obs, info = env.reset()
    done = False
    steps = 0
    while not done and steps < 50:
        action = agent.act(obs)
        obs, reward, done, _, info = env.step(action)
        steps += 1
    print("Test abgeschlossen. Agent hat überlebt?", not done)
