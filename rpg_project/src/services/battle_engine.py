"""
BattleEngine: Service für rundenbasierte Kämpfe zwischen zwei Entitäten.
- Startet einen Kampf
- Führt Kampfschritte aus
- Gibt den aktuellen Kampfstatus zurück

Alle Werte werden aus den Konfigurationsdateien geladen (datengetriebenes Design).
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel
from rpg_project.src.models.core import Opponent, Item
from enum import Enum

class BattleState(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"

class EntityState(BaseModel):
    id: str
    name: str
    hp: int
    max_hp: int
    atk: int
    defense: int
    is_player: bool

class BattleStatus(BaseModel):
    state: BattleState
    turn: int
    attacker: str
    defender: str
    entities: Dict[str, EntityState]
    winner: Optional[str] = None


# Einfacher In-Memory-BattleStore für Demo/Test
class BattleStore:
    def __init__(self):
        self._battles: dict[str, BattleStatus] = {}

    def create_battle(self, battle_id: str, player: EntityState, opponent: EntityState) -> BattleStatus:
        battle = BattleStatus(
            state=BattleState.IN_PROGRESS,
            turn=1,
            attacker=player.id,
            defender=opponent.id,
            entities={player.id: player, opponent.id: opponent},
            winner=None,
        )
        self._battles[battle_id] = battle
        return battle

    def step(self, battle_id: str) -> BattleStatus:
        battle = self._battles.get(battle_id)
        if not battle:
            raise RuntimeError("Kein Kampf aktiv")
        if battle.state != BattleState.IN_PROGRESS:
            raise RuntimeError("Kampf ist nicht mehr aktiv")
        attacker = battle.entities[battle.attacker]
        defender = battle.entities[battle.defender]
        dmg = max(1, attacker.atk - defender.defense)
        defender.hp = max(0, defender.hp - dmg)
        if defender.hp <= 0:
            battle.state = BattleState.FINISHED
            battle.winner = attacker.id
        if battle.state == BattleState.IN_PROGRESS:
            battle.attacker, battle.defender = battle.defender, battle.attacker
            battle.turn += 1
        self._battles[battle_id] = battle
        return battle

    def get_state(self, battle_id: str) -> Optional[BattleStatus]:
        return self._battles.get(battle_id)
