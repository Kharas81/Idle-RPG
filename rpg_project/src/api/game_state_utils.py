
"""
game_state_utils.py
Hilfsfunktionen für Spielzustand und Weltlogik. Enthält defensive Checks und Typannotationen.
"""

from typing import Dict, Any, Tuple, Optional
from rpg_project.src.models.world import Tile, WorldMap

def get_worldmap_from_state(state: Dict[str, Any]) -> WorldMap:
    """
    Erzeugt ein WorldMap-Objekt aus dem aktuellen Spielzustand.
    Defensive Checks für fehlende Felder.
    """
    tiles = [Tile(**t) for t in state.get("tiles", [])]
    goal_tile = next((t for t in tiles if getattr(t, "type", None) == "goal"), None)
    goal = (goal_tile.x, goal_tile.y) if goal_tile else (0, 0)
    return WorldMap(
        width=state.get("width", 0),
        height=state.get("height", 0),
        tiles=tiles,
        start=(0, 0),
        goal=goal
    )

def get_player_pos(state: Dict[str, Any]) -> Tuple[int, int]:
    """
    Gibt die aktuelle Spielerposition als (x, y) zurück.
    """
    for ent in state.get("entities", []):
        if ent.get("type") == "player":
            return (ent.get("x", 0), ent.get("y", 0))
    return (0, 0)

def set_player_pos(state: Dict[str, Any], pos: Tuple[int, int]) -> None:
    """
    Setzt die Spielerposition auf das gegebene Tupel (x, y).
    Defensive Prüfung auf Tupel und Existenz.
    """
    if not (isinstance(pos, tuple) and len(pos) == 2):
        return
    for ent in state.get("entities", []):
        if ent.get("type") == "player":
            ent["x"], ent["y"] = pos
            break
