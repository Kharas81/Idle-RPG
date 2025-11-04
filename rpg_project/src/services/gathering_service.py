from typing import Any

from rpg_project.src.models.resource import Resource


class GatheringService:
    def __init__(self, world_map: dict[str, Any]):
        self.world_map = world_map

    def gather(self, player, position) -> Resource:
        """Sammelt Ressource an gegebener Position, fügt sie dem Inventar hinzu.
        Gibt die gesammelte Resource zurück oder None, falls nichts da ist.
        """
        # Position als String-Schlüssel '(x,y)'
        if isinstance(position, tuple):
            pos_key = f"({position[0]},{position[1]})"
        else:
            pos_key = str(position)
        tile = self.world_map.get("tiles", {}).get(pos_key)
        if tile and tile.get("resource"):
            res = Resource(**tile["resource"])
            player.inventory.append({"name": res.name, "type": res.type, "amount": res.amount})
            # Ressource entfernen (einmalig sammelbar)
            del tile["resource"]
            return res
        return None
