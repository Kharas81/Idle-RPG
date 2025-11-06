"""TalentService: Verwaltung und Anwendung von Talenten
"""
from rpg_project.src.models.character import Character
from rpg_project.src.models.talent import TalentTree


class TalentService:
    def __init__(self, talent_tree: TalentTree):
        self.talent_tree = talent_tree

    def can_learn(self, character: Character, talent_id: str) -> bool:
        # Prüfe, ob Voraussetzungen erfüllt sind
        talent = self.talent_tree.talents.get(talent_id)
        if not talent:
            return False
        # Bereits gelernt?
        if hasattr(character, "talents") and talent_id in character.talents:
            return False
        # Prüfe Voraussetzungen
        for pre in talent.prerequisites:
            if not hasattr(character, "talents") or pre not in character.talents:
                return False
        return True

    def learn_talent(self, character: Character, talent_id: str) -> bool:
        if not self.can_learn(character, talent_id):
            return False
        # Explizite Prüfung: Wenn stats zu Beginn None, kein stat_bonus-Talent lernen
        if hasattr(character, "stats") and character.stats is None:
            talent = self.talent_tree.talents.get(talent_id)
            if talent:
                for effect in talent.effects:
                    if effect.effect_type == "stat_bonus":
                        return False
        talent = self.talent_tree.talents.get(talent_id)
        # Prüfe, ob alle Effekte angewendet werden können
        if talent:
            for effect in talent.effects:
                if effect.effect_type == "stat_bonus":
                    if not hasattr(character, "stats") or character.stats is None:
                        return False
        if not hasattr(character, "talents"):
            character.talents = []
        # Effekte anwenden und prüfen, ob sie erfolgreich waren
        if not self.apply_talent_effects(character, talent_id):
            return False
        character.talents.append(talent_id)
        return True

    def apply_talent_effects(self, character: Character, talent_id: str) -> bool:
        talent = self.talent_tree.talents.get(talent_id)
        if not talent:
            return False
        for effect in talent.effects:
            # Effektziel muss gesetzt sein
            if effect.effect_type == "stat_bonus":
                if effect.target is not None and effect.value is not None:
                    # Nur int/float als stat_bonus zulassen
                    if isinstance(effect.value, (int, float)):
                        if not hasattr(character, "stats") or character.stats is None:
                            return False
                        character.stats[effect.target] = character.stats.get(effect.target, 0) + int(effect.value)
            elif effect.effect_type == "percent_bonus":
                if effect.target is not None and effect.value is not None:
                    # Nur float als percent_bonus zulassen
                    if isinstance(effect.value, float):
                        if not hasattr(character, "percent_bonuses"):
                            character.percent_bonuses = {}
                        character.percent_bonuses[effect.target] = character.percent_bonuses.get(effect.target, 0) + effect.value
            # Weitere Effekttypen können ergänzt werden
        return True
