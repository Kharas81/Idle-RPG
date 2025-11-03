from rl.environment import RpgEnv
from stable_baselines3.common.env_checker import check_env

def test_rl_environment():
    env = RpgEnv()
    check_env(env)

test_rl_environment()