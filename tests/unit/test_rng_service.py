"""
Unit-Test für RNGService: Seed, Reset, Determinismus
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import pytest
from rpg_project.src.services.rng_service import RNGService

def test_rng_determinism():
    rng = RNGService()
    rng.seed(42)
    seq1 = [rng.randint(1, 100) for _ in range(5)]
    rng.reset()
    seq2 = [rng.randint(1, 100) for _ in range(5)]
    assert seq1 == seq2
    # Anderer Seed ergibt andere Sequenz
    rng.seed(99)
    seq3 = [rng.randint(1, 100) for _ in range(5)]
    assert seq1 != seq3
