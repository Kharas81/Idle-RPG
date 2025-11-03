"""
RNGService: Zentraler Zufallszahlengenerator mit Seed für 100% reproduzierbare Runs.
"""
import random
from typing import Optional

class RNGService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._rng = random.Random()
            cls._instance._seed = None
        return cls._instance

    def seed(self, seed_value: int):
        self._seed = seed_value
        self._rng.seed(seed_value)

    def randint(self, a: int, b: int) -> int:
        return self._rng.randint(a, b)

    def random(self) -> float:
        return self._rng.random()

    def get_seed(self) -> Optional[int]:
        return self._seed

    def reset(self):
        if self._seed is not None:
            self._rng.seed(self._seed)

# Singleton-Instanz
rng_service = RNGService()
