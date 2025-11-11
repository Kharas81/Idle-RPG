"""
Definiert Spaces für RL-Umgebung (Gymnasium)
"""
from gymnasium import spaces

# Beispiel: Diskreter Aktionsraum
ACTION_SPACE = spaces.Discrete(3)  # 0=Bewegen, 1=Kämpfen, 2=Craften

# Beispiel: Beobachtungsraum
OBSERVATION_SPACE = spaces.Box(low=0, high=100, shape=(5,), dtype=int)
