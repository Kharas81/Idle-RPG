from rpg_project.src.models.world import WorldMap, Tile
from typing import Tuple

class MovementService:
    @staticmethod
    def can_move(world: WorldMap, pos: Tuple[int, int], direction: str) -> bool:
        dx, dy = 0, 0
        if direction == "up":
            dy = -1
        elif direction == "down":
            dy = 1
        elif direction == "left":
            dx = -1
        elif direction == "right":
            dx = 1
        else:
            return False
        new_x, new_y = pos[0] + dx, pos[1] + dy
        # Prüfe Kartenbegrenzung
        if not (0 <= new_x < world.width and 0 <= new_y < world.height):
            return False
        # Prüfe, ob das Ziel ein begehbares Feld ist
        for tile in world.tiles:
            if tile.x == new_x and tile.y == new_y:
                return tile.type != "wall"
        return False

    @staticmethod
    def move(world: WorldMap, pos: Tuple[int, int], direction: str) -> Tuple[int, int]:
        if MovementService.can_move(world, pos, direction):
            dx, dy = 0, 0
            if direction == "up":
                dy = -1
            elif direction == "down":
                dy = 1
            elif direction == "left":
                dx = -1
            elif direction == "right":
                dx = 1
            return (pos[0] + dx, pos[1] + dy)
        return pos
