# **GDD \- 3\. Skills & Effekte (config/skills.json5)**

**Ziel (B2.1):** Definition aller Skills (Fähigkeiten) und Status-Effekte (Buffs/Debuffs) unter Verwendung des flexiblen "Effekt-Motors" (B1).

## **Glossar**

* **ID:** Die eindeutige Kennung des Skills.  
* **Klasse(n):** Legt fest, welche Heldenklassen diesen Skill nutzen oder lernen können.  
* **Kosten:** Definiert den Ressourcenverbrauch (z.B. Mana, Stamina) beim Auslösen.  
* **Effekte (Liste) (B1):** Das Kernstück. Eine Liste von Aktionen, die der Skill nacheinander ausführt. Dies erlaubt komplexe Skills (z.B. Schaden \+ Heilung \+ Statuseffekt) ohne Code-Änderungen.

## **Syntax-Beispiel (B1, B2.2)**

So wird ein Skill in config/skills.json5 definiert. Das System (S8) iteriert durch die effekte-Liste.

// config/skills.json5  
{  
  "skill\_shield\_bash": {  
    "name": "Schildschlag",  
    "class": \["Krieger", "Kleriker"\],  
    "costs": { "type": "Stamina", "amount": 5 },  
    "description": "Verursacht Schaden basierend auf DEF, kann lähmen.",  
      
    // B1: Der Effekt-Motor. Dies ist eine Liste von Aktionen.  
    "effekte": \[  
      {  
        "type": "damage",  
        "multiplier": "self.def \* 0.5", // Schaden basiert auf Verteidigung  
        "damage\_type": "Physical"  
      },  
      {  
        "type": "apply\_effect",         // Wendet einen Statuseffekt an  
        "effect\_id": "stun",            // Die ID aus Teil B dieses Dokuments  
        "duration": 1,  
        "chance": 0.5                   // 50% Chance, den Effekt anzuwenden  
      }  
    \]  
  },  
    
  "skill\_life\_drain": {  
    "name": "Lebensentzug",  
    "class": \["Magier", "Kleriker"\],  
    "costs": { "type": "Mana", "amount": 10 },  
    "description": "Verursacht 10 Schaden und heilt um denselben Betrag.",  
      
    // B1: Beispiel für einen Skill mit zwei verschiedenen Aktionstypen  
    "effekte": \[  
      {  
        "type": "damage",  
        "amount": 10,  
        "damage\_type": "Shadow"  
      },  
      {  
        "type": "heal",  
        "amount": 10  
      }  
    \]  
  }  
}

## **A) Skills (Fähigkeiten)**

| ID | Name | Klasse(n) | Kosten (Typ, Menge) | Effekte (Liste von Aktionen) (B1) | Beschreibung |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Tier 1 (Basis)** |  |  |  |  |  |
| basic\_attack | Basis-Angriff | Alle | \- | \[ {"type": "damage", "multiplier": "self.atk"} \] | Ein normaler Angriff. |
| heavy\_smash | Schwerer Schlag | Krieger | Stamina: 10 | \[ {"type": "damage", "multiplier": "self.atk \* 1.5"} \] | Ein langsamer, aber starker Angriff. |
| quick\_strike | Schneller Stich | Schurke | Stamina: 3 | \[ {"type": "damage", "multiplier": "self.atk \* 0.8"} \] | Ein schneller Angriff, der wenig Schaden macht. |
| skill\_arrow\_shot | Pfeilschuss | Schurke | Stamina: 5 | \[ {"type": "damage", "multiplier": "self.atk \* 1.0"} \] | Ein Standard-Fernkampfangriff. |
| skill\_fireball | Feuerball | Magier | Mana: 10 | \[ {"type": "damage", "amount": 20, "damage\_type": "Fire"}, {"type": "apply\_effect", "effect\_id": "burn", "duration": 3} \] | Verursacht Feuerschaden und verbrennt das Ziel. |
| skill\_heal\_light | Leichte Heilung | Kleriker | Mana: 15 | \[ {"type": "heal", "amount": 40} \] | Heilt ein einzelnes Ziel. |
| skill\_shield\_bash | Schildschlag | Krieger, Kleriker | Stamina: 5 | \[ {"type": "damage", "multiplier": "self.def \* 0.5"}, {"type": "apply\_effect", "effect\_id": "stun", "duration": 1, "chance": 0.5} \] | Verursacht Schaden basierend auf DEF, kann lähmen. |
| skill\_defensive\_stance | Verteidigungshaltung | Krieger, Kleriker | Stamina: 5 | \[ {"type": "apply\_effect\_self", "effect\_id": "def\_up", "duration": 3} \] | Erhöht die eigene Verteidigung. |
| skill\_war\_cry | Kriegsruf | Krieger | Mana: 15 | \[ {"type": "apply\_effect\_aoe", "target": "ALLIES", "effect\_id": "atk\_up", "duration": 3} \] | Erhöht den Angriff aller Verbündeten. |
| skill\_intimidating\_shout | Einschüchternder Ruf | Krieger | Mana: 10 | \[ {"type": "apply\_effect\_aoe", "target": "ENEMIES", "effect\_id": "def\_down", "duration": 3} \] | Senkt die Verteidigung aller Gegner. |
| skill\_apply\_poison | Gift auftragen | Schurke | Mana: 10 | \[ {"type": "apply\_effect", "effect\_id": "poison", "duration": 4} \] | Vergiftet ein einzelnes Ziel. |
| skill\_throw\_net | Netz werfen | Schurke | Stamina: 5 | \[ {"type": "apply\_effect", "effect\_id": "stun", "duration": 2} \] | Wirft ein Netz, das ein Ziel lähmt. |
| **Tier 2 (Fortgeschritten)** |  |  |  |  |  |
| skill\_ice\_arrow | Eispfeil | Magier | Mana: 8 | \[ {"type": "damage", "amount": 10, "damage\_type": "Ice"}, {"type": "apply\_effect", "effect\_id": "slow", "duration": 3} \] | Verursacht Eisschaden und verlangsamt das Ziel. |
| skill\_mana\_burn | Manabrand | Magier, Schurke | Mana: 5 | \[ {"type": "damage\_resource", "resource": "mana", "amount": 25} \] | Verbrennt 25 Mana des Ziels. |
| skill\_summon\_skeleton | Skelett beschwören | Magier | Mana: 20 | \[ {"type": "summon", "entity\_id": "skeleton\_warrior", "max\_summons": 2} \] | Beschwört ein schwaches Skelett. |
| skill\_steal\_gold | Gold stehlen | Schurke | Stamina: 0 | \[ {"type": "steal", "resource": "gold", "min": 5, "max": 15} \] | Stiehlt dem Ziel Gold. |
| skill\_poison\_sting | Giftstachel | Schurke | Stamina: 5 | \[ {"type": "damage", "amount": 3, "damage\_type": "Nature"}, {"type": "apply\_effect", "effect\_id": "poison", "duration": 4} \] | Verursacht geringen Schaden und vergiftet. |
| skill\_steal\_item | Gegenstand stehlen | Schurke | Stamina: 0 | \[ {"type": "steal\_item", "item\_type": "Consumable", "chance": 0.3} \] | Stiehlt dem Ziel einen zufälligen 'Consumable'. |
| skill\_life\_drain | Lebensentzug | Magier, Kleriker | Mana: 10 | \[ {"type": "damage", "amount": 10}, {"type": "heal", "amount": 10} \] | Verursacht 10 Schaden und heilt um denselben Betrag. |
| skill\_deep\_cut | Tiefer Schnitt | Krieger, Schurke | Stamina: 10 | \[ {"type": "damage", "multiplier": "self.atk \* 1.2"}, {"type": "apply\_effect", "effect\_id": "bleed", "duration": 3} \] | Verursacht Schaden und 'Bluten'. |
| skill\_whirlwind | Wirbelwind | Krieger | Stamina: 20 | \[ {"type": "damage\_aoe", "target": "ENEMIES", "multiplier": "self.atk \* 0.8"} \] | Greift alle nahen Gegner an. |
| skill\_taunt | Spott | Krieger | Mana: 5 | \[ {"type": "apply\_effect\_self", "effect\_id": "taunting", "duration": 2} \] | Zwingt alle Gegner, den Anwender anzugreifen. |
| skill\_regeneration | Regeneration | Kleriker | Mana: 15 | \[ {"type": "apply\_effect\_self", "effect\_id": "regen\_hp", "duration": 4} \] | Heilt 20 HP pro Runde für 4 Runden. |
| skill\_berserk\_rage | Berserkerwut | Krieger | HP: 10% | \[ {"type": "apply\_effect\_self", "effect\_id": "atk\_up\_major", "duration": 3} \] | Nur unter 30% HP. Erhöht ATK massiv, senkt DEF. |
| **Tier 3 (Elite)** |  |  |  |  |  |
| skill\_lightning\_bolt | Blitzschlag | Magier | Mana: 15 | \[ {"type": "damage", "amount": 50, "damage\_type": "Lightning"}, {"type": "apply\_effect", "effect\_id": "stun", "duration": 1, "chance": 0.2} \] | Trifft ein Ziel, kann lähmen. |
| skill\_apply\_fear | Furcht einflößen | Kleriker, Schurke | Mana: 20 | \[ {"type": "apply\_effect", "effect\_id": "fear", "duration": 2} \] | Lässt ein Ziel 2 Runden lang aussetzen. |
| skill\_summon\_harpy | Harpyie beschwören | Magier | Mana: 30 | \[ {"type": "summon", "entity\_id": "cliff\_harpy", "max\_summons": 1} \] | Beschwört eine Harpyie. |
| skill\_pillage | Plündern | Schurke | Stamina: 10 | \[ {"type": "damage", "multiplier": "self.atk \* 1.0"}, {"type": "apply\_effect\_self", "effect\_id": "steal\_item\_chance", "duration": 1} \] | Verursacht Schaden, nächste Aktion ist steal\_item. |
| skill\_heal\_medium | Mittlere Heilung | Kleriker | Mana: 30 | \[ {"type": "heal", "amount": 150} \] | Heilt ein einzelnes Ziel. |
| skill\_firestorm | Feuersturm | Magier | Mana: 40 | \[ {"type": "damage\_aoe", "target": "ENEMIES", "amount": 80, "damage\_type": "Fire"}, {"type": "apply\_effect", "effect\_id": "burn", "duration": 3} \] | Trifft alle Gegner mit Feuer. |
| skill\_invisibility | Unsichtbarkeit | Schurke | Mana: 25 | \[ {"type": "apply\_effect\_self", "effect\_id": "invisible", "duration": 3} \] | Macht 3 Runden unsichtbar (bricht bei Angriff). |
| **Tier 4 (Legendär)** |  |  |  |  |  |
| skill\_on\_death\_explode | Explosion bei Tod | Alle (Gegner) | Passiv | \[ {"type": "on\_death\_trigger", "effect": {"type": "damage\_aoe", "amount": 30}} \] | Passiv: Explodiert bei Tod. |
| skill\_summon\_orc\_raider | Ork-Plünderer rufen | Magier (Gegner) | Mana: 40 | \[ {"type": "summon", "entity\_id": "orc\_raider", "max\_summons": 2} \] | Beschwört einen Ork-Plünderer. |
| skill\_heal\_area | Flächenheilung | Kleriker | Mana: 50 | \[ {"type": "heal\_aoe", "target": "ALLIES", "amount": 100} \] | Heilt alle Verbündeten um 100 HP. |
| skill\_meteor | Meteor | Magier | Mana: 80 | \[ {"type": "damage\_aoe", "target": "ENEMIES", "amount": 300, "damage\_type": "Fire"}, {"type": "apply\_effect", "effect\_id": "stun", "duration": 1} \] | Verursacht massiven Feuerschaden und lähmt. |
| skill\_time\_stop | Zeitstopp | Magier (Legendär) | Mana: 100 | \[ {"type": "apply\_effect\_aoe", "target": "ENEMIES", "effect\_id": "stun", "duration": 2} \] | Lähmt alle Gegner für 2 Runden. |

## **B) Status-Effekte (Buffs & Debuffs)**

(Definiert die IDs, die im apply\_effect-Typ des Effekt-Motors verwendet werden.)

| ID | Name | Technische Wirkung (Modifikator / Tick-Effekt) (B2.5) | Standard Dauer (Runden) |
| :---- | :---- | :---- | :---- |
| **Debuffs (Negativ)** |  |  |  |
| burn | Brennen | {"type": "damage", "amount": 5, "damage\_type": "Fire"} (Tick-Schaden) | 3 |
| poison | Vergiftet | {"type": "damage", "amount": 3, "damage\_type": "Nature"} (Tick-Schaden) | 4 |
| bleed | Bluten | {"type": "damage", "amount": 4, "ignores\_def": true} (Tick-Schaden) | 3 |
| stun | Gelähmt | {"type": "skip\_turn"} (Aktion aussetzen) | 1 |
| slow | Verlangsamt | {"speed\_multiplier": 0.5} (Stat-Modifikator) | 3 |
| def\_down | Verteidigung Runter | {"def\_multiplier": 0.75} (Stat-Modifikator) | 3 |
| atk\_down | Schwäche | {"atk\_multiplier": 0.75} (Stat-Modifikator) | 3 |
| fear | Furcht | {"type": "skip\_turn"} (Aktion aussetzen) | 2 |
| taunting | Verspottet | {"type": "force\_target", "target": "self"} (Erzwingt Ziel) | 2 |
| **Buffs (Positiv)** |  |  |  |
| def\_up | Verteidigung Hoch | {"def\_multiplier": 1.5} (Stat-Modifikator) | 3 |
| atk\_up | Angriff Hoch | {"atk\_multiplier": 1.25} (Stat-Modifikator) | 3 |
| speed\_up | Geschwindigkeit Hoch | {"speed\_multiplier": 1.5} (Stat-Modifikator) | 5 (Minuten) |
| atk\_up\_major | Angriff Hoch (Stark) | {"atk\_multiplier": 2.0, "def\_multiplier": 0.5} (Stat-Modifikator) | 3 (Runden) |
| regen\_hp | Regeneration (HP) | {"type": "heal", "amount": 20} (Tick-Heilung) | 4 |
| invisible | Unsichtbar | {"type": "set\_flag", "flag": "IS\_INVISIBLE"} (Status-Flag) | 3 |
| steal\_item\_chance | Plündern-Bereit | {"type": "set\_flag", "flag": "NEXT\_ACTION\_STEAL"} (Status-Flag) | 1 |

