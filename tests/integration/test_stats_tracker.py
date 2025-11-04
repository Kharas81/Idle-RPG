"""Integrationstest für StatsTracker: 10 Schleime besiegen und Statistik prüfen
"""
from rpg_project.src.services.stats_tracker import StatsTracker


def test_slimes_defeated_stat():
    tracker = StatsTracker()
    # Simuliere 10 besiegte Schleime
    for _ in range(10):
        tracker.on_event("ON_ENEMY_DEFEATED", {"opponent_type": "slime"})
    stats = tracker.get_stats()
    assert stats["slimes_defeated"] == 10
