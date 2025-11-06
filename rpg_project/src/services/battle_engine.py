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
        # Nutze die neue, vollständige Skill-Liste
        path = Path("config/skills_full.json5")
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
        # Kosten prüfen (Mana/Stamina)
        costs = skill.get("costs")
        if costs:
            if costs["type"].lower() == "mana":
                if user.mana < costs["amount"]:
                    raise RuntimeError("Nicht genug Mana")
                user.mana -= costs["amount"]
            elif costs["type"].lower() == "stamina":
                # Falls Stamina implementiert ist, hier abziehen
                pass
        # Effekte interpretieren
        for eff in skill.get("effekte", []):
            typ = eff.get("type")
            if typ == "damage":
                # Multiplikator oder fixer Wert
                if "multiplier" in eff:
                    # Eval mit Vorsicht, nur auf user-Attribute
                    try:
                        multiplier = eff["multiplier"]
                        dmg = eval(str(multiplier), {}, {"self": user})
                        dmg = int(dmg)
                    except Exception:
                        dmg = 1
                else:
                    dmg = eff.get("amount", 0)
                # Damage-Type und Defense berücksichtigen
                dmg = max(1, dmg - getattr(target, "defense", 0))
                target.hp = max(0, target.hp - dmg)
            elif typ == "heal":
                amount = eff.get("amount", 0)
                user.hp = min(user.max_hp, user.hp + amount)
            elif typ == "apply_effect":
                # Status-Effekt auf Ziel anwenden
                effect_id = eff.get("effect_id", "")
                duration = eff.get("duration", 1)
                # Name aus effect_id ableiten
                effect = Effect(name=effect_id.capitalize(), duration=duration)
                target.effects.append(effect)
            elif typ == "apply_effect_self":
                effect_id = eff.get("effect_id", "")
                duration = eff.get("duration", 1)
                effect = Effect(name=effect_id.capitalize(), duration=duration)
                user.effects.append(effect)
            # Weitere Typen wie apply_effect_aoe, etc. können hier ergänzt werden
        # Cooldown setzen (optional, falls in Daten vorhanden)
        if "cooldown" in skill:
            battle.cooldowns.setdefault(user_id, {})[skill_name] = skill["cooldown"]
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
