"""BattleEngine: Service für rundenbasierte Kämpfe zwischen zwei Entitäten.
- Startet einen Kampf
- Führt Kampfschritte aus
- Gibt den aktuellen Kampfstatus zurück

Alle Werte werden aus den Konfigurationsdateien geladen (datengetriebenes Design).
"""
from enum import Enum
from pathlib import Path

import json5
from pydantic import BaseModel

from rpg_project.src.models.effects import Effect


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
    effects: list[Effect] = []  # Aktive Effekte
    mana: int = 100  # Für Skillkosten

class BattleStatus(BaseModel):
    state: BattleState
    turn: int
    attacker: str
    defender: str
    entities: dict[str, EntityState]
    winner: str | None = None

    cooldowns: dict[str, dict[str, int]] = {}  # cooldowns[entity_id][skill_name] = turns


# Einfacher In-Memory-BattleStore für Demo/Test
class BattleStore:
    def __init__(self):
        self._battles: dict[str, BattleStatus] = {}
        # Skills aus Config laden
        self.skills = self._load_skills()

    def _load_skills(self):
        path = Path("config/skills.json5")
        with path.open("r", encoding="utf-8") as f:
            return json5.load(f)

    def create_battle(self, battle_id: str, player: EntityState, opponent: EntityState) -> BattleStatus:
        # Effekte/Cooldowns/Mana initialisieren
        player.effects = []
        opponent.effects = []
        player.mana = 100
        opponent.mana = 100
        cooldowns = {player.id: {}, opponent.id: {}}
        battle = BattleStatus(
            state=BattleState.IN_PROGRESS,
            turn=1,
            attacker=player.id,
            defender=opponent.id,
            entities={player.id: player, opponent.id: opponent},
            winner=None,
            cooldowns=cooldowns,
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

        # Effekte ticken lassen (z.B. Brennen)
        for entity in battle.entities.values():
            new_effects = []
            for effect in entity.effects:
                if effect.damage_per_tick:
                    entity.hp = max(0, entity.hp - effect.damage_per_tick)
                effect.duration -= 1
                if effect.duration > 0:
                    new_effects.append(effect)
            entity.effects = new_effects

        # Cooldowns runterzählen
        for eid in battle.cooldowns:
            for skill in list(battle.cooldowns[eid].keys()):
                battle.cooldowns[eid][skill] = max(0, battle.cooldowns[eid][skill] - 1)
                if battle.cooldowns[eid][skill] == 0:
                    del battle.cooldowns[eid][skill]

        # Standardangriff, falls kein Skill genutzt wurde
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

    def use_skill(self, battle_id: str, user_id: str, skill_name: str) -> BattleStatus:
        battle = self._battles.get(battle_id)
        if not battle:
            raise RuntimeError("Kein Kampf aktiv")
        if battle.state != BattleState.IN_PROGRESS:
            raise RuntimeError("Kampf ist nicht mehr aktiv")
        user = battle.entities[user_id]
        target_id = battle.defender if battle.attacker == user_id else battle.attacker
        target = battle.entities[target_id]
        skill = self.skills.get(skill_name)
        if not skill:
            raise RuntimeError(f"Skill {skill_name} nicht gefunden")
        # Cooldown prüfen
        if battle.cooldowns.get(user_id, {}).get(skill_name, 0) > 0:
            raise RuntimeError("Skill ist im Cooldown")
        # Kosten prüfen
        if user.mana < skill.get("cost", 0):
            raise RuntimeError("Nicht genug Mana")
        user.mana -= skill.get("cost", 0)
        # Schaden anwenden
        if "damage" in skill:
            dmg = max(1, skill["damage"] - target.defense)
            target.hp = max(0, target.hp - dmg)
        # Heilung
        if "heal" in skill:
            user.hp = min(user.max_hp, user.hp + skill["heal"])
        # Effekte anwenden
        for eff in skill.get("effects", []):
            effect = Effect(**eff)
            target.effects.append(effect)
        # Cooldown setzen
        battle.cooldowns.setdefault(user_id, {})[skill_name] = skill.get("cooldown", 0)
        # Rundenwechsel wie bei step
        if target.hp <= 0:
            battle.state = BattleState.FINISHED
            battle.winner = user.id
        if battle.state == BattleState.IN_PROGRESS:
            battle.attacker, battle.defender = battle.defender, battle.attacker
            battle.turn += 1
        self._battles[battle_id] = battle
        return battle

    def get_state(self, battle_id: str) -> BattleStatus | None:
        return self._battles.get(battle_id)
