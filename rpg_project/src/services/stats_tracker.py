"""StatsTracker: Sammelt Statistiken über die Spieler-Session via Event-System
"""


class StatsTracker:
    def __init__(self):
        self.stats: dict[str, int] = {}

    def on_event(self, event_type: str, data: dict):
        # Beispiel: Gegner besiegt
        if event_type == "ON_ENEMY_DEFEATED":
            enemy_type = data.get("opponent_type", "unknown")
            if enemy_type == "slime":
                self.stats["slimes_defeated"] = self.stats.get("slimes_defeated", 0) + 1
            # Weitere Gegnerarten können ergänzt werden
        # Weitere Events können ergänzt werden

    def get_stats(self) -> dict[str, int]:
        return self.stats.copy()
