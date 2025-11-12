"""
Integrationstest für die RL-Umgebung (RpgEnv)
"""
import pytest
from rpg_project.src.rl.environment import RpgEnv

def test_rl_env_runs():
    env = RpgEnv()
    obs, info = env.reset()
    import numpy as np
    assert isinstance(obs, (list, np.ndarray))
    done = False
    steps = 0
    while not done and steps < 10:
        obs, reward, done, _, info = env.step(env.action_space.sample())
        assert isinstance(obs, (list, np.ndarray))
        steps += 1
    env.close()
