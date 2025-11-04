"""API-Endpunkt: /character/stats
"""
from fastapi import APIRouter

from rpg_project.src.services.stats_tracker import StatsTracker

router = APIRouter()

# Dummy: In der echten App wird der StatsTracker pro Session/Spieler verwaltet
stats_tracker = StatsTracker()

@router.get("/character/stats")
def get_character_stats():
    return stats_tracker.get_stats()
