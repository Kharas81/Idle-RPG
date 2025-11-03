
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from rpg_project.src.models.world import WorldMap, Tile
from rpg_project.src.services.movement_service import MovementService

def make_test_world():
    return WorldMap(
        width=3,
        height=3,
        tiles=[
            Tile(x=0, y=0, type="start"),
            Tile(x=1, y=0, type="floor"),
            Tile(x=2, y=0, type="wall"),
            Tile(x=0, y=1, type="floor"),
            Tile(x=1, y=1, type="floor"),
            Tile(x=2, y=1, type="goal")
        ],
        start=(0, 0),
        goal=(2, 1),
        name="Testmap"
    )

def test_move_into_wall():
    world = make_test_world()
    pos = (1, 0)
    # Rechts ist eine Wand
    new_pos = MovementService.move(world, pos, "right")
    assert new_pos == pos

def test_move_to_floor():
    world = make_test_world()
    pos = (0, 0)
    new_pos = MovementService.move(world, pos, "right")
    assert new_pos == (1, 0)

def test_move_out_of_bounds():
    world = make_test_world()
    pos = (0, 0)
    new_pos = MovementService.move(world, pos, "up")
    assert new_pos == pos

def test_move_to_goal():
    world = make_test_world()
    pos = (1, 1)
    new_pos = MovementService.move(world, pos, "right")
    assert new_pos == (2, 1)
