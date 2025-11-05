from rpg_project.src.models.world import Tile, WorldMap

def get_worldmap_from_state(state):
    tiles = [Tile(**t) for t in state["tiles"]]
    goal_tile = next((t for t in tiles if t.type == "goal"), None)
    goal = (goal_tile.x, goal_tile.y) if goal_tile else (0, 0)
    return WorldMap(width=state["width"], height=state["height"], tiles=tiles, start=(0,0), goal=goal)

def get_player_pos(state):
    for ent in state["entities"]:
        if ent["type"] == "player":
            return (ent["x"], ent["y"])
    return (0,0)

def set_player_pos(state, pos):
    if not (isinstance(pos, tuple) and len(pos) == 2):
        return
    for ent in state["entities"]:
        if ent["type"] == "player":
            ent["x"], ent["y"] = pos
            break
