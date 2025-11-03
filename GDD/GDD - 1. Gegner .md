# **GDD \- 1\. Gegner (config/opponents.json5)**

**Ziel:** Definition aller Gegner-Stammdaten unter Verwendung eines flexiblen "Archetyp" (Mixin)-Systems (Vorschlag B1).

**System (B1):** Statt "Vererbung" (inherits\_from) nutzen wir "Komposition" (archetypes). Das System kombiniert die Archetypen in der angegebenen Reihenfolge. Ein späterer Archetyp oder eine Überschreibung hat Vorrang.

## **A) Gegner-Archetypen (Die Bausteine)**

(Dies sind die "Lego-Bausteine". Sie definieren gemeinsame Eigenschaften und werden in config/archetypes/ gespeichert.)

### **1\. Basis-Archetypen (Kreaturentyp)**

// config/archetypes/base.json5  
{  
  "base\_goblin": {  
    "stats": { "hp": 30, "atk": 5, "def": 3, "spd": 8 },  
    "faction": "goblins",  
    "skills": \["basic\_attack"\],  
    "loot\_table\_id": "lt\_goblin\_base"  
  },  
  "base\_orc": {  
    "stats": { "hp": 80, "atk": 12, "def": 6, "spd": 5 },  
    "faction": "orcs",  
    "skills": \["basic\_attack", "heavy\_smash"\],  
    "loot\_table\_id": "lt\_orc\_base"  
  },  
  "base\_undead": {  
    "stats": { "hp": 50, "atk": 8, "def": 5, "spd": 6 },  
    "faction": "undead",  
    "skills": \["basic\_attack"\],  
    "loot\_table\_id": "lt\_undead\_base",  
    "special": \["Immun: Gift", "Bluten", "Schwach: Feuer"\]  
  },  
  "base\_beast": {  
    "stats": { "hp": 40, "atk": 10, "def": 4, "spd": 12 },  
    "faction": "beasts",  
    "skills": \["basic\_attack"\],  
    "loot\_table\_id": "lt\_beast\_base"  
  },  
  "base\_construct": {  
    "stats": { "hp": 100, "atk": 15, "def": 15, "spd": 3 },  
    "faction": "constructs",  
    "skills": \["heavy\_smash"\],  
    "loot\_table\_id": "lt\_construct\_base",  
    "special": \["Immun: Gift", "Bluten", "Stun"\]  
  },  
  "base\_bandit": {  
    "stats": { "hp": 60, "atk": 7, "def": 5, "spd": 9 },  
    "faction": "bandits",  
    "skills": \["basic\_attack"\],  
    "loot\_table\_id": "lt\_bandit\_base"  
  },  
  "base\_harpy": {  
    "stats": { "hp": 50, "atk": 8, "def": 4, "spd": 15 },  
    "faction": "harpyien",  
    "skills": \["basic\_attack"\],  
    "loot\_table\_id": "lt\_harpy\_base"  
  },  
  "base\_elemental": {  
    "stats": { "hp": 70, "atk": 10, "def": 10, "spd": 7 },  
    "faction": "elementals",  
    "skills": \["basic\_attack"\],  
    "loot\_table\_id": "lt\_elemental\_base"  
  }  
}

### **2\. Rollen-Archetypen (Spezialisierung)**

// config/archetypes/roles.json5  
{  
  "role\_magic\_light": {  
    // Fügt Mana hinzu, ändert Stats leicht, fügt Skill hinzu  
    "stats": { "hp": "+10", "def": "-1", "mana": 50 },  
    "skills": \["skill\_heal\_light"\]  
  },  
  "role\_magic\_fire": {  
    "stats": { "mana": 50 },  
    "skills": \["skill\_fireball"\]  
  },  
  "role\_magic\_ice": {  
    "stats": { "mana": 50 },  
    "skills": \["skill\_ice\_arrow"\]  
  },  
  "role\_ranged": {  
    "stats": { "atk": "-1", "spd": "+2" },  
    "skills": \["skill\_arrow\_shot"\],  
    "ai\_policy": "Aggressive\_Ranged"  
  },  
  "role\_tank": {  
    "stats": { "hp": "+50", "def": "+10", "atk": "-2" },  
    "skills": \["skill\_taunt"\],  
    "ai\_policy": "Aggressive\_Tank"  
  }  
}

## **B) Gegner-Varianten (Echte Gegner)**

(Das sind die 52 Gegner, die im Spiel in config/opponents.json5 definiert werden. Sie kombinieren die Archetypen.)

| ID | Name | Archetypen (B1) | Überschreibungen (Stats, Skills, etc.) | KI-Policy | XP |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **GOBLINS** |  |  |  |  |  |
| goblin\_scout | Goblin Späher | \["base\_goblin"\] | stats: { "atk": 8, "spd": 12 }, skills: \["quick\_strike"\] | Coward | 10 |
| goblin\_shaman | Goblin-Schamane | \["base\_goblin", "role\_magic\_light"\] | stats: { "hp": 40, "def": 4 } | Healer | 15 |
| goblin\_archer | Goblin-Bogenschütze | \["base\_goblin", "role\_ranged"\] | stats: { "atk": 7 } | (aus role\_ranged) | 12 |
| goblin\_trapper | Goblin-Fallensteller | \["base\_goblin"\] | stats: { "def": 5, "spd": 10 }, skills: \["skill\_throw\_net"\] | Saboteur\_Stun | 13 |
| goblin\_berserker | Goblin-Berserker | \["base\_goblin"\] | stats: { "hp": 50, "atk": 10, "def": 1 }, skills: \["skill\_berserk\_rage"\] | Aggressive\_LowHP | 18 |
| goblin\_horde\_leader | Goblin-Hordenführer | \["base\_goblin"\] | stats: { "hp": 80, "atk": 8, "def": 5 }, skills: \["skill\_war\_cry"\] | Support\_Buffer | 30 |
| **ORKS** |  |  |  |  |  |
| orc\_brute | Ork-Schläger | \["base\_orc"\] | stats: { "hp": 120, "def": 8 } | Aggressive | 25 |
| orc\_war\_drummer | Ork-Kriegstrommler | \["base\_orc"\] | stats: { "hp": 70, "atk": 5, "mana": 30 }, skills: \["skill\_war\_cry", "skill\_intimidating\_shout"\] | Support\_Buffer | 30 |
| orc\_raider | Ork-Plünderer | \["base\_orc"\] | stats: { "spd": 7 }, skills: \["skill\_pillage"\] | Aggressive\_Item | 28 |
| orc\_blademaster | Ork-Klingenmeister | \["base\_orc"\] | stats: { "hp": 90, "atk": 14, "spd": 8 }, skills: \["skill\_whirlwind"\] | Aggressive\_AOE | 40 |
| orc\_shaman | Ork-Schamane | \["base\_orc", "role\_magic\_fire"\] | stats: { "atk": 8, "mana": 50 }, skills: \["skill\_heal\_light"\] | Aggressive\_Magic | 45 |
| orc\_warchief | Ork-Kriegshäuptling | \["base\_orc"\] | stats: { "hp": 250, "atk": 18, "def": 10 }, skills: \["skill\_war\_cry", "skill\_summon\_orc\_raider"\] | Spawner\_Buffer | 100 |
| **UNTOTE** |  |  |  |  |  |
| shadow\_wisp | Schattengeist | \["base\_undead"\] | stats: { "atk": 0, "def": 10, "spd": 10 }, skills: \["skill\_mana\_burn"\] | Saboteur\_Mana | 20 |
| necromancer\_acolyte | Nekromanten-Akolyt | \["base\_undead"\] | stats: { "hp": 40, "atk": 5, "mana": 30 }, skills: \["skill\_summon\_skeleton"\] | Spawner | 25 |
| bloodfiend\_acolyte | Blutsauger-Akolyt | \["base\_undead"\] | stats: { "hp": 60, "atk": 10, "mana": 20 }, skills: \["skill\_life\_drain"\] | Vampiric | 22 |
| skeleton\_warrior | Skelett-Krieger | \["base\_undead"\] | stats: { "hp": 30, "atk": 6, "def": 3 } | Aggressive | 10 |
| skeleton\_archer | Skelett-Schütze | \["base\_undead", "role\_ranged"\] | stats: { "hp": 25, "atk": 8, "spd": 7 } | (aus role\_ranged) | 12 |
| zombie\_shambler | Schlurfender Zombie | \["base\_undead"\] | stats: { "hp": 80, "atk": 10, "spd": 2 }, skills: \["skill\_slam"\] | Aggressive\_Slow | 15 |
| ghoul\_scavenger | Ghul-Aasfresser | \["base\_undead"\] | stats: { "atk": 9, "spd": 9 }, skills: \["skill\_apply\_poison"\] | Aggressive\_Poisoner | 20 |
| wraith | Schemen | \["base\_undead", "role\_magic\_ice"\] | stats: { "hp": 70, "atk": 0, "def": 8, "mana": 40 }, skills: \["skill\_apply\_fear"\] | Saboteur\_Fear | 35 |
| dread\_knight | Schreckensritter | \["base\_undead", "role\_tank"\] | stats: { "hp": 150, "atk": 15, "def": 12 }, skills: \["skill\_life\_drain", "skill\_intimidating\_shout"\] | Vampiric\_Tank | 70 |
| lich\_apprentice | Lich-Lehrling | \["base\_undead", "role\_magic\_fire"\] | stats: { "hp": 100, "atk": 5, "mana": 100 }, skills: \["skill\_ice\_arrow", "skill\_summon\_skeleton"\] | Spawner\_Magic | 80 |
| **WILDTIERE (BEASTS)** |  |  |  |  |  |
| spider\_queen | Spinnenkönigin | \["base\_beast"\] | stats: { "hp": 120, "atk": 10, "def": 10, "mana": 40 }, skills: \["skill\_poison\_sting", "skill\_summon\_spiderling"\] | Spawner\_Poisoner | 60 |
| giant\_wolf | Riesenwolf | \["base\_beast"\] | stats: { "hp": 50, "atk": 12, "spd": 14 }, skills: \["skill\_deep\_cut"\] | Aggressive\_Fast | 15 |
| dire\_bear | Schreckensbär | \["base\_beast", "role\_tank"\] | stats: { "hp": 130, "atk": 15, "def": 8, "spd": 6 }, skills: \["heavy\_smash"\] | Aggressive\_Tank | 40 |
| manticore\_cub | Mantikor-Junges | \["base\_beast"\] | stats: { "hp": 90, "atk": 12, "mana": 30 }, skills: \["skill\_poison\_sting"\] | Aggressive\_Poisoner | 35 |
| wyvern\_hatchling | Wyvern-Schlüpfling | \["base\_beast"\] | stats: { "hp": 70, "atk": 10, "spd": 15 }, skills: \["skill\_apply\_poison"\] | Aggressive\_Flying | 30 |
| forest\_troll | Waldtroll | \["base\_beast"\] | stats: { "hp": 100, "atk": 14, "def": 5 }, skills: \["heavy\_smash", "skill\_regeneration"\] | Aggressive\_Regen | 45 |
| **KONSTRUKTE (CONSTRUCTS)** |  |  |  |  |  |
| iron\_golem | Eisengolem | \["base\_construct", "role\_tank"\] | stats: { "hp": 150, "def": 25 } | Aggressive\_Tank | 50 |
| obsidian\_golem | Obsidiangolem | \["base\_construct", "role\_magic\_fire"\] | stats: { "hp": 120, "def": 20 } | Aggressive\_Magic | 60 |
| ancient\_guardian | Antiker Wächter | \["base\_construct", "role\_tank"\] | stats: { "hp": 200, "atk": 18, "def": 18 }, skills: \["skill\_shield\_bash"\] | Aggressive\_Tank | 80 |
| arcane\_sentry | Arkaner Wächter | \["base\_construct"\] | stats: { "hp": 80, "atk": 0, "mana": 100 }, skills: \["skill\_mana\_burn"\] | Saboteur\_Mana | 40 |
| clockwork\_spider | Uhrwerk-Spinne | \["base\_construct"\] | stats: { "hp": 40, "atk": 8, "spd": 12 }, skills: \["skill\_apply\_poison"\] | Aggressive\_Poisoner | 25 |
| **BANDITEN (MENSCHEN)** |  |  |  |  |  |
| bandit\_thug | Banditen-Schläger | \["base\_bandit"\] | skills: \["skill\_steal\_gold"\] | Saboteur\_Gold | 15 |
| bandit\_archer | Banditen-Schütze | \["base\_bandit", "role\_ranged"\] | stats: { "atk": 8 } | (aus role\_ranged) | 17 |
| bandit\_cutpurse | Banditen-Beutelschneider | \["base\_bandit"\] | stats: { "atk": 5, "spd": 12 }, skills: \["skill\_steal\_item", "quick\_strike"\] | Saboteur\_Item | 20 |
| bandit\_hedge\_knight | Banditen-Heckenritter | \["base\_bandit", "role\_tank"\] | stats: { "hp": 90, "atk": 10, "def": 8 }, skills: \["skill\_shield\_bash"\] | Aggressive\_Tank | 30 |
| bandit\_leader | Banditen-Anführer | \["base\_bandit"\] | stats: { "hp": 120, "atk": 12, "def": 10 }, skills: \["skill\_war\_cry", "skill\_deep\_cut"\] | Support\_Buffer | 50 |
| **HARPYIEN** |  |  |  |  |  |
| cliff\_harpy | Klippen-Harpyie | \["base\_harpy"\] | skills: \["skill\_steal\_item"\] | Saboteur\_Item | 20 |
| harpy\_screecher | Harpyien-Kreischerin | \["base\_harpy"\] | stats: { "atk": 5, "mana": 30 }, skills: \["skill\_intimidating\_shout"\] | Support\_Debuffer | 25 |
| harpy\_stormcaller | Harpyien-Sturmruferin | \["base\_harpy", "role\_magic\_fire"\] | stats: { "atk": 8, "mana": 40 }, skills: \["skill\_lightning\_bolt"\] | Aggressive\_Magic | 35 |
| harpy\_queen | Harpyien-Königin | \["base\_harpy", "role\_magic\_fire"\] | stats: { "hp": 150, "atk": 12, "mana": 50 }, skills: \["skill\_summon\_harpy", "skill\_lightning\_bolt"\] | Spawner\_Magic | 80 |
| **ELEMENTARE** |  |  |  |  |  |
| mire\_imp | Instabiler Morast-Wichtel | \["base\_elemental"\] | stats: { "hp": 20, "atk": 5, "def": 0 }, skills: \["skill\_on\_death\_explode"\] | Aggressive\_Kamikaze | 10 |
| fire\_elemental | Feuer-Elementar | \["base\_elemental", "role\_magic\_fire"\] | stats: { "hp": 80, "atk": 0, "mana": 50 } | Aggressive\_Magic | 30 |
| ice\_elemental | Eis-Elementar | \["base\_elemental", "role\_magic\_ice"\] | stats: { "hp": 80, "atk": 0, "mana": 50 } | Aggressive\_Magic | 30 |
| earth\_elemental | Erd-Elementar | \["base\_elemental", "role\_tank"\] | stats: { "hp": 120, "atk": 15, "def": 15, "spd": 3 }, skills: \["skill\_shield\_bash"\] | Aggressive\_Tank | 40 |
| storm\_elemental | Sturm-Elementar | \["base\_elemental"\] | stats: { "hp": 70, "atk": 0, "mana": 60, "spd": 15 }, skills: \["skill\_lightning\_bolt"\] | Aggressive\_Magic | 40 |
| void\_elemental | Leeren-Elementar | \["base\_elemental"\] | stats: { "hp": 100, "atk": 10, "mana": 80 }, skills: \["skill\_mana\_burn"\] | Saboteur\_Mana | 50 |
| magma\_golem | Magma-Golem | \["base\_elemental", "role\_tank", "role\_magic\_fire"\] | stats: { "hp": 150, "atk": 16, "def": 12 }, skills: \["heavy\_smash"\] | Aggressive\_Tank | 70 |

