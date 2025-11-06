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
        # Prüfe, ob stat_bonus angewendet werden soll, aber keine Stats vorhanden sind
        talent = self.talent_tree.talents.get(talent_id)
        if talent:
            for effect in talent.effects:
                if effect.effect_type == "stat_bonus" and (not hasattr(character, "stats") or character.stats is None):
                    return False
        if not hasattr(character, "talents"):
            character.talents = []
        character.talents.append(talent_id)
        self.apply_talent_effects(character, talent_id)
        return True

    def apply_talent_effects(self, character: Character, talent_id: str):
        talent = self.talent_tree.talents.get(talent_id)
        if not talent:
            return
        for effect in talent.effects:
            # Effektziel muss gesetzt sein
            if effect.effect_type == "stat_bonus":
                if effect.target is not None and effect.value is not None:
                    # Nur int/float als stat_bonus zulassen
                    if isinstance(effect.value, (int, float)):
                        character.stats[effect.target] = character.stats.get(effect.target, 0) + int(effect.value)
            elif effect.effect_type == "percent_bonus":
                if effect.target is not None and effect.value is not None:
                    # Nur float als percent_bonus zulassen
                    if isinstance(effect.value, float):
                        if not hasattr(character, "percent_bonuses"):
                            character.percent_bonuses = {}
                        character.percent_bonuses[effect.target] = character.percent_bonuses.get(effect.target, 0) + effect.value
            # Weitere Effekttypen können ergänzt werden
