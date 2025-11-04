def merge_skills(archetype_skills, opponent_skills, overwrite=False):
    """
    Merged Skills aus Archetypen und Gegnerdaten, ohne Duplikate.
    Reihenfolge: erst Archetypen, dann Gegnerdaten. Bei overwrite nur Gegnerdaten.
    """
    if overwrite:
        return list(opponent_skills) if opponent_skills else []
    result = []
    for skill in archetype_skills or []:
        if skill not in result:
            result.append(skill)
    for skill in opponent_skills or []:
        if skill not in result:
            result.append(skill)
    return result
from pathlib import Path
from typing import TypeVar

import json5

T = TypeVar("T")

class ConfigLoader:
    @staticmethod
    def load_config(path: str, model: type[T]) -> list[T]:
        from pydantic import TypeAdapter
        file_path = Path(path)
        with file_path.open("r", encoding="utf-8") as f:
            data = json5.load(f)
        # Falls data ein Dict ist (wie bei talents), Werte extrahieren
        if isinstance(data, dict):
            data = list(data.values())

        # Spezialbehandlung für Opponent: Archetypen auflösen und mergen
        if model.__name__ == "Opponent":
            # Lade alle Archetypen-Dateien
            import glob
            archetype_dir = Path(__file__).parent.parent.parent.parent / "config" / "archetypes"
            archetype_files = glob.glob(str(archetype_dir / "*.json5"))
            archetypes = {}
            for afile in archetype_files:
                with open(afile, "r", encoding="utf-8") as f:
                    arch = json5.load(f)
                    archetypes.update(arch)
            # Merge-Logik für jeden Gegner
            merged = []
            for opp in data:
                base = {}
                archetype_skills = []
                # Archetypen in Reihenfolge anwenden
                for arch_id in opp.get("archetypes", []):
                    arch = archetypes.get(arch_id, {})
                    for k, v in arch.items():
                        if k == "skills":
                            for skill in v:
                                if skill not in archetype_skills:
                                    archetype_skills.append(skill)
                        elif isinstance(v, dict):
                            base.setdefault(k, {}).update(v)
                        elif isinstance(v, list):
                            base.setdefault(k, []).extend(v)
                        else:
                            base[k] = v
                    if base.get("id") == "goblin_scout":
                        print(f"DEBUG goblin_scout skills nach Archetypen: {base.get('skills')}")
                # Überschreibungen aus Gegnerobjekt anwenden
                skills_overwrite = opp.get("skills_overwrite", False)
                for k, v in opp.items():
                    if k == "stats" and v:
                        base.setdefault("stats", {}).update(v)
                    elif k != "skills" and k != "skills_overwrite":
                        base[k] = v
                # Skills zusammenführen
                opponent_skills = opp.get("skills", [])
                base["skills"] = merge_skills(archetype_skills, opponent_skills, opp.get("skills_overwrite", False))
                merged.append(base)
            data = merged

        adapter = TypeAdapter(list[model])
        return adapter.validate_python(data)
