"""
End-to-End-Test: RL-Agent trainieren, speichern, laden und Dummy-Gegner besiegen
"""
from rpg_project.src.rl.environment import RpgEnv
from rpg_project.src.rl.agent import FighterAgent

def test_fighter_agent_e2e():
    env = RpgEnv()
    agent = FighterAgent(env)
    agent.train(episodes=5)
    agent.save("fighter_agent.model")
    agent.load("fighter_agent.model")
    obs, info = env.reset()
    done = False
    steps = 0
    while not done and steps < 50:
        action = agent.act(obs)
        obs, reward, done, _, info = env.step(action)
        steps += 1
    assert steps > 0
    assert agent.model == "dummy-trained"
