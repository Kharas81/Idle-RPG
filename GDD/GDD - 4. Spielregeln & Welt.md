# **GDD \- 4\. Spielregeln & Welt v2 (Überarbeitet)**

**Ziel:** Definition aller übergreifenden Spielregeln, der KI-Logik, der Talentbäume und der Welt-Inhalte (NPCs, Quests, Fraktionen).

## **Glossar (B2.12)**

* **RPG-Systeme (S7):** Grundlegende Spielregeln wie XP, Level und Klassen.  
* **Talentbäume (S12):** Spezialisierungen für die Heldenklassen.  
* **KI-Policy (S9):** Ein Verhaltens-Skript, das einer Gegner-KI zugewiesen wird.  
* **Fraktion (S17):** Eine Gruppierung von NPCs/Gegnern, die sich eine Reputation teilen.  
* **NPC (S18):** Ein "Non-Player Character", eine Entität, mit der interagiert werden kann.  
* **Quest (S18):** Eine Aufgabe, die ein NPC vergibt und die Belohnungen gewährt.

## **A) S7: RPG-Systeme (config/game\_rules.json5)**

**Ziel (B2.1):** Definition der Kern-Progressionsregeln, auf die das RPGSystem (S7) zugreift.

### **1\. XP-Kurve**

(Wie viel XP braucht der Spieler für das nächste Level?)

| Level | Benötigte XP |
| :---- | :---- |
| 1 \-\> 2 | 100 XP |
| 2 \-\> 3 | 250 XP |
| 3 \-\> 4 | 500 XP |
| 4 \-\> 5 | 850 XP |
| 5 \-\> 6 | 1300 XP |
| 6 \-\> 7 | 1900 XP |
| 7 \-\> 8 | 2700 XP |
| 8 \-\> 9 | 3800 XP |
| 9 \-\> 10 | 5000 XP |

**Formel (B2.6):** $ (Level^{2.2}) \\times 40 \+ 60 $, gerundet

### **2\. Heldenklassen**

(Welche Rollen kann der Spieler übernehmen?)

| Klasse | Beschreibung | Start-Stats (ATK/DEF/INT/SPD) | Berufsvorschläge |
| :---- | :---- | :---- | :---- |
| Krieger | Ein robuster Nahkämpfer, der sich auf Stärke und Verteidigung verlässt. | 12 / 10 / 5 / 8 | Schmiedekunst, Alchemie |
| Magier | Ein fragiler, aber mächtiger Fernkämpfer, der elementare Kräfte nutzt. | 5 / 6 / 15 / 9 | Schneiderei, Alchemie |
| Schurke | Ein schneller und listiger Angreifer, der Gifte, Fallen und Diebstahl nutzt. | 9 / 8 / 7 / 12 | Schneiderei, Alchemie |
| Kleriker | Ein unterstützender Kämpfer, der Heilmagie und defensive Buffs nutzt. | 8 / 9 / 12 / 7 | Schmiedekunst, Schneiderei |

## **B) S12: Talentbäume (config/talents.json5)**

**Ziel (B2.1):** Definition der Talentbäume, die der TalentService (S12) nutzt.

### **1\. Krieger-Baum (Fokus: Stärke, Verteidigung, Physisch)**

| ID (B2.9) | Tier | Name / Effekt |
| :---- | :---- | :---- |
| warrior\_robust\_1 | 1 | \+10% Max HP (Passiv) |
| warrior\_weapon\_1 | 1 | \+5% Physischer Schaden (Passiv) |
| warrior\_shield\_1 | 2 | \+10% Verteidigung, wenn Schild ausgerüstet (Passiv) |
| warrior\_skill\_1 | 2 | Schaltet Skill skill\_deep\_cut frei (verursacht "Bluten") |
| warrior\_speed\_1 | 2 | \+10% Geschwindigkeit (Passiv) |
| warrior\_defense\_2 | 3 | \+50% Verteidigung durch skill\_defensive\_stance (Verbessert Skill) |
| warrior\_skill\_2 | 3 | Schaltet Skill skill\_whirlwind frei |

### **2\. Magier-Baum (Fokus: Intelligenz, Mana, Elementar)**

| ID (B2.9) | Tier | Name / Effekt |
| :---- | :---- | :---- |
| mage\_mana\_1 | 1 | \+10% Max Mana (Passiv) |
| mage\_elemental\_1 | 1 | \+5% Magieschaden (Passiv) |
| mage\_fire\_1 | 2 | \+10% Feuerschaden (Beeinflusst skill\_fireball) |
| mage\_ice\_1 | 2 | Schaltet Skill skill\_ice\_arrow frei |
| mage\_mana\_2 | 2 | Stellt 1 Mana pro Tick im Kampf wieder her (Passiv) |
| mage\_fire\_2 | 3 | \+20% Chance, dass "Brennen" 2 Runden länger dauert (Passiv) |
| mage\_mastery\_1 | 3 | \-10% Manakosten auf alle Skills (Passiv) |
| mage\_skill\_1 | 3 | Schaltet Skill skill\_firestorm frei |

### **3\. Schurke-Baum (Fokus: Geschwindigkeit, List, Gifte)**

| ID (B2.9) | Tier | Name / Effekt |
| :---- | :---- | :---- |
| rogue\_speed\_1 | 1 | \+5% Geschwindigkeit und \+5% Ausweichen (Passiv) |
| rogue\_poison\_1 | 1 | \+10% Giftschaden (Passiv) |
| rogue\_utility\_1 | 2 | Schaltet Skill skill\_steal\_item frei |
| rogue\_skill\_1 | 2 | Schaltet Skill skill\_invisibility frei |
| rogue\_crit\_1 | 2 | \+5% Kritische Trefferchance (Passiv) |
| rogue\_poison\_2 | 3 | skill\_apply\_poison trifft jetzt 2x (Verbessert Skill) |
| rogue\_mastery\_1 | 3 | "Stehlen" kostet keine Aktion (Passiv) |

### **4\. Kleriker-Baum (Fokus: Heilung, Verteidigung, Unterstützung)**

| ID (B2.9) | Tier | Name / Effekt |
| :---- | :---- | :---- |
| cleric\_heal\_1 | 1 | \+10% Effekt von Heilzaubern (Passiv) |
| cleric\_defense\_1 | 1 | \+5% Verteidigung und \+5% Magie-Resistenz (Passiv) |
| cleric\_utility\_1 | 2 | Schaltet Skill skill\_regeneration frei |
| cleric\_skill\_1 | 2 | Schaltet Skill skill\_heal\_area frei (Flächenheilung) |
| cleric\_buff\_1 | 2 | skill\_defensive\_stance hält 2 Runden länger (Verbessert Skill) |
| cleric\_mastery\_1 | 3 | Wiederbeleben (außerhalb des Kampfes) kostet 50% weniger Mana (Passiv) |
| cleric\_skill\_2 | 3 | Schaltet Skill skill\_apply\_fear frei |

## **C) S9: KI-Verhalten (ai\_policy in opponents.json5)**

**Ziel (B2.1):** Definition der Verhaltens-Richtlinien, die der AIService (S9) nutzt.

| Policy-ID | Beschreibung | Pseudocode (B2.4) | Verwendet von (Beispiele) |
| :---- | :---- | :---- | :---- |
| Aggressive | Nutzt immer den stärksten physischen Skill. Greift Ziel mit niedrigsten HP an. | target \= lowest\_hp\_enemy; use(strongest\_physical\_skill, target) | orc\_brute, iron\_golem |
| Aggressive\_Magic | Wie "Aggressive", nutzt aber primär magische Skills. | target \= lowest\_hp\_enemy; use(strongest\_magic\_skill, target) | fire\_elemental, orc\_shaman |
| Aggressive\_Ranged | Hält Abstand und nutzt Fernkampf-Skills. | target \= lowest\_hp\_enemy; if (distance(target) \< 3): move\_away() else: use(ranged\_skill, target) | goblin\_archer, skeleton\_archer |
| Aggressive\_Kamikaze | Versucht, schnell zu sterben, um on\_death\_explode auszulösen. | target \= closest\_enemy; move\_to(target) | mire\_imp |
| Aggressive\_LowHP | Nutzt Spezial-Skills (z.B. Berserkerwut), wenn HP niedrig sind. | if (self.hp \< 0.3): use(berserk\_rage) else: use(basic\_attack) | goblin\_berserker |
| Aggressive\_Fast | Nutzt schnelle Angriffe (quick\_strike), um Initiative zu gewinnen. | target \= lowest\_hp\_enemy; use(quick\_strike, target) | giant\_wolf |
| Aggressive\_Slow | Nutzt langsame, starke Angriffe (skill\_slam). | target \= lowest\_hp\_enemy; use(skill\_slam, target) | zombie\_shambler |
| Aggressive\_AOE | Priorisiert Angriffe, die mehrere Ziele treffen. | if (enemies\_nearby \> 1): use(aoe\_skill) else: use(basic\_attack) | orc\_blademaster |
| Aggressive\_Tank | Nutzt skill\_taunt, wenn Verbündete angegriffen werden. | target \= ally\_being\_attacked; if (target): use(skill\_taunt) else: use(basic\_attack) | dire\_bear, dread\_knight |
| Aggressive\_Item | Nutzt skill\_pillage, um Items zu zerstören. | target \= player; use(skill\_pillage, target) | orc\_raider |
| Aggressive\_Poisoner | Hält poison-Debuff auf dem Ziel aufrecht. | target \= player; if (target.has\_effect("poison") \== false): use(skill\_apply\_poison) else: use(basic\_attack) | ghoul\_scavenger, manticore\_cub |
| Aggressive\_Flying | (Für zukünftige Logik) Kann nicht von Boden-Nahkampf getroffen werden. | (Logik in BattleEngine) | wyvern\_hatchling |
| Aggressive\_Regen | Kämpft aggressiv, da es sich passiv heilt. | target \= lowest\_hp\_enemy; use(strongest\_physical\_skill, target) | forest\_troll |
| Coward | Wenn HP \< 30%, versucht zu fliehen oder nutzt Verteidigungs-Skills. | if (self.hp \< 0.3): use(flee\_skill) else: use(basic\_attack) | goblin\_scout |
| Healer | Wenn ein Verbündeter (oder es selbst) \< 50% HP hat, nutzt es Heilung. | target \= lowest\_hp\_ally(hp \< 0.5); if (target): use(heal\_skill, target) else: use(basic\_attack) | goblin\_shaman |
| Support\_Buffer | Priorisiert das Buffen von Verbündeten (atk\_up). | target \= strongest\_ally; if (target.has\_effect("atk\_up") \== false): use(buff\_skill, target) else: use(basic\_attack) | orc\_war\_drummer, bandit\_leader |
| Support\_Debuffer | Priorisiert das Debuffen von Gegnern. | target \= strongest\_enemy; if (target.has\_effect("def\_down") \== false): use(debuff\_skill, target) else: use(basic\_attack) | harpy\_screecher |
| Saboteur\_Mana | Greift primär das Mana des Ziels an, ignoriert HP. | target \= player; if (target.mana \> 0): use(skill\_mana\_burn, target) else: use(basic\_attack) | shadow\_wisp, arcane\_sentry |
| Saboteur\_Gold | Nutzt "Gold stehlen", solange der Spieler Gold hat. | target \= player; if (target.gold \> 0): use(skill\_steal\_gold, target) else: use(basic\_attack) | bandit\_thug |
| Saboteur\_Item | Versucht, "Gegenstand stehlen" zu nutzen. | target \= player; use(skill\_steal\_item, target) | cliff\_harpy, bandit\_cutpurse |
| Saboteur\_Stun | Versucht, das Ziel handlungsunfähig zu machen (skill\_throw\_net). | target \= strongest\_enemy; if (target.has\_effect("stun") \== false): use(skill\_throw\_net, target) | goblin\_trapper |
| Saboteur\_Fear | Versucht, das Ziel mit skill\_apply\_fear zu lähmen. | target \= player; use(skill\_apply\_fear, target) | wraith |
| Spawner | Priorisiert das Beschwören von Dienern, solange das Limit nicht erreicht ist. | if (self.summons \< max\_summons): use(summon\_skill) else: use(basic\_attack) | necromancer\_acolyte |
| Spawner\_Poisoner | Kombiniert "Spawner" mit "Poisoner". | if (self.summons \< max\_summons): use(summon\_skill) else: use(skill\_apply\_poison) | spider\_queen |
| Spawner\_Buffer | Beschwört Diener und bufft diese. | if (self.summons \< max\_summons): use(summon\_skill) else: use(buff\_skill, strongest\_ally) | orc\_warchief |
| Spawner\_Magic | Beschwört Diener und greift mit Magie an. | if (self.summons \< max\_summons): use(summon\_skill) else: use(magic\_skill, lowest\_hp\_enemy) | lich\_apprentice, harpy\_queen |
| Vampiric | Nutzt "Lebensentzug", wenn HP \< 100%. | if (self.hp \< self.max\_hp): use(skill\_life\_drain) else: use(basic\_attack) | bloodfiend\_acolyte |
| Vampiric\_Tank | Kombiniert "Vampiric" mit "Aggressive\_Tank". | if (self.hp \< self.max\_hp): use(skill\_life\_drain) else: use(skill\_taunt) | dread\_knight |

## **D) S17/S18: Welt (Fraktionen, NPCs, Quests, Dialoge)**

**Ziel (B2.1):** Definition der sozialen Struktur der Welt, der Charaktere und der Aufgaben.

### **1\. Fraktionen (config/factions.json5)**

| ID | Name | Beschreibung | Start-Reputation |
| :---- | :---- | :---- | :---- |
| city\_guard | Stadtwache von Startburg | Beschützt die Stadt. Hassen Banditen und Goblins. | 50 |
| bandits | Die Roten Klingen | Banditenkartell. Hassen die Stadtwache. | \-50 |
| goblins | Goblin-Stamm | Chaotisch. Plündern alles. | \-20 |
| orcs | Ork-Clan | Stark und diszipliniert. Oft im Krieg mit Menschen. | \-30 |
| undead | Die Ruhelosen | Skelette, Geister und Nekromanten. Hassen alles Lebende. | \-100 |
| constructs | Konstrukte | Magische Golems. Dienen ihren Erbauern loyal. | 0 |
| dwarven\_guild | Zwergen-Gilde | Neutrale Bergleute und Handwerker. | 0 |
| beasts | Wildtiere | Neutrale Tiere des Waldes. | 0 |
| elementals | Elementare | Chaotisch-neutrale Geister der Natur. | \-10 |
| harpyien | Harpyien-Schwarm | Aggressive, diebische Kreaturen. | \-15 |

**Beziehungs-Tabelle (B2.10)** (Beispielhafte Startwerte)

| Fraktion | city\_guard | bandits | goblins | orcs | undead |
| :---- | :---- | :---- | :---- | :---- | :---- |
| city\_guard | 100 | \-100 | \-50 | \-20 | 0 |
| bandits | \-100 | 100 | 10 | 0 | 0 |
| goblins | \-50 | 10 | 100 | 0 | \-10 |
| orcs | \-20 | 0 | 0 | 100 | 0 |
| undead | 0 | 0 | \-10 | 0 | 100 |

### **2\. NPCs (B1: Mark & Jane)**

| ID | Name | Standort | Fraktion | Anmerkung |
| :---- | :---- | :---- | :---- | :---- |
| guard\_captain\_markus | Hauptmann Markus | Startburg (Tor) | city\_guard | \- |
| blacksmith\_boris | Schmied Boris | Startburg (Schmiede) | Neutral | \- |
| nurse\_jane | **Pflegerin Jane** | Startburg (Tempel) | Neutral | (Anspielung auf deine Freundin, **Jane**) |
| citizen\_mark | **Mark, der Bürger** | Startburg (Marktplatz) | Neutral | (Anspielung auf dich, **Mark**) |
| alchemist\_filius | Alchemist Filius | Startburg (Alchemielabor) | Neutral | \- |
| tailor\_selina | Schneiderin Selina | Startburg (Schneiderei) | Neutral | \- |
| npc\_traveling\_merchant | Wandernder Händler | (Dynamisch) | Neutral | (Wird von S27 gespawnt) |
| npc\_dwarven\_merchant | Zwergenhändler | (Dynamisch) | dwarven\_guild | (Wird von S27 gespawnt) |

### **3\. Quests (config/quests.json5) (B1: Mark & Jane)**

| ID | Titel | Auftraggeber (NPC) | Ziel (Typ, Ziel, Menge) | Belohnung (Gold, XP, Items, Rep) |
| :---- | :---- | :---- | :---- | :---- |
| q\_goblin\_plague | Die Goblin-Plage | guard\_captain\_markus | {"type": "kill", "target\_faction": "goblins", "count": 10} | {"gold": 50, "xp": 100, "rep": {"city\_guard": 10}} |
| q\_iron\_shortage | Eisenerz-Knappheit | blacksmith\_boris | {"type": "gather", "item\_id": "iron\_ore", "count": 20} | {"gold": 100, "xp": 50, "item": "blueprint\_iron\_sword"} |
| q\_cure\_for\_the\_sick | Ein Heilmittel für die Kranken | nurse\_jane | {"type": "gather", "item\_id": "red\_herb", "count": 5} | {"gold": 20, "xp": 75, "item": "potion\_heal\_small:3", "rep": {"city\_guard": 5}} |
| q\_lost\_amulet | Das verlorene Amulett | citizen\_mark | {"type": "find\_item", "item\_id": "janes\_lost\_amulet"} | {"gold": 50, "xp": 50, "item": "janes\_worn\_amulet:1"} |
| q\_orc\_threat | Die Ork-Bedrohung | guard\_captain\_markus | {"type": "kill", "target\_id": "orc\_warchief", "count": 1} | {"gold": 300, "xp": 500, "rep": {"city\_guard": 30}} |
| q\_silk\_delivery | Seidenlieferung | tailor\_selina | {"type": "gather", "item\_id": "shadow\_silk", "count": 10} | {"gold": 150, "xp": 100, "item": "pattern\_silk\_robe:1"} |

### **4\. Dialoge (Beispiel) (B1: Mark & Jane)**

(Dies ist, wie die dialogues.json5-Dateien strukturiert sein werden)

// config/dialogues/dialog\_markus\_intro.json5  
{  
  "start\_node": "node\_1",  
  "nodes": {  
    "node\_1": {  
      "npc\_text": "Seid gegrüßt, Reisender. Die Straßen sind gefährlich.",  
      "player\_choices": \[  
        { "text": "Was ist das Problem?", "next\_node": "node\_2" },  
        { "text": "Ich habe keine Zeit.", "next\_node": "END" }  
      \]  
    },  
    "node\_2": {  
      "npc\_text": "Goblins\! Sie überfallen unsere Händler. Könnt Ihr uns helfen?",  
      "player\_choices": \[  
        { "text": "Ja, ich helfe.", "action": "ACCEPT\_QUEST", "quest\_id": "q\_goblin\_plague", "next\_node": "node\_3" },  
        { "text": "Ich kann nicht.", "next\_node": "END" }  
      \]  
    },  
    "node\_3": {  
      "npc\_text": "Ausgezeichnet\! Meldet Euch bei mir, wenn Ihr 10 von ihnen erledigt habt.",  
      "player\_choices": \[ { "text": "Verstanden.", "next\_node": "END" } \]  
    }  
  }  
}

// config/dialogues/dialog\_jane\_intro.json5  
{  
  "start\_node": "node\_1",  
  "nodes": {  
    "node\_1": {  
      "npc\_text": "Oh, Götter sei Dank. Wir brauchen dringend Hilfe. Ein seltsames Fieber grassiert, und uns gehen die Kräuter aus.",  
      "player\_choices": \[  
        { "text": "Was braucht Ihr?", "next\_node": "node\_2" },  
        { "text": "Schrecklich. Ich kann nicht helfen.", "next\_node": "END" }  
      \]  
    },  
    "node\_2": {  
      "npc\_text": "Nur 5 Rote Kräuter. Könntet Ihr sie für mich im Wald suchen? Ich kann Euch nicht viel bezahlen, aber Ihr würdet Leben retten.",  
      "player\_choices": \[  
        { "text": "Ich werde sehen, was ich tun kann.", "action": "ACCEPT\_QUEST", "quest\_id": "q\_cure\_for\_the\_sick", "next\_node": "END" },  
        { "text": "Das ist es mir nicht wert.", "next\_node": "END" }  
      \]  
    }  
  }  
}

// NEU: config/dialogues/dialog\_mark\_intro.json5 (B1)  
{  
  "start\_node": "node\_1",  
  "nodes": {  
    "node\_1": {  
      "npc\_text": "Ach, Ihr müsst mir helfen\! Ich habe ein Amulett verloren... es ist ein Geschenk für Jane. Es muss mir beim Marktplatz aus der Tasche gefallen sein.",  
      "player\_choices": \[  
        { "text": "Ein Amulett für Jane, die Pflegerin?", "next\_node": "node\_2" },  
        { "text": "Pech gehabt.", "next\_node": "END" }  
      \]  
    },  
    "node\_2": {  
      "npc\_text": "Ja, genau die\! Ich... nun, es ist mir wichtig. Banditen wurden in der Nähe gesehen. Ich fürchte, sie haben es mitgenommen. Könntet Ihr es für mich suchen?",  
      "player\_choices": \[  
        { "text": "Ich halte die Augen offen.", "action": "ACCEPT\_QUEST", "quest\_id": "q\_lost\_amulet", "next\_node": "END" },  
        { "text": "Ich habe keine Zeit für so etwas.", "next\_node": "END" }  
      \]  
    }  
  }  
}

## **E) S19: Begleiter (config/pets.json5)**

**Ziel (B2.1):** Definition der Begleiter, die der PetService (S19) und der AIService (S9/S19) nutzen.

| ID | Name | Basis-Stats (HP/ATK/DEF) | Skills | AI-Policy |
| :---- | :---- | :---- | :---- | :---- |
| pet\_wolf | Treuer Wolf | 50 / 10 / 5 | basic\_attack | Pet\_Aggressive (Greift Ziel des Besitzers an) |
| pet\_fairy | Heil-Fee | 30 / 0 / 0 (Mana: 100\) | skill\_heal\_light | Pet\_Healer (Heilt Besitzer, wenn HP \< 50%) |
| pet\_baby\_golem | Baby-Golem | 100 / 5 / 10 | basic\_attack, skill\_taunt | Pet\_Tank (Nutzt Taunt, wenn HP des Besitzers \< 70%) |
| pet\_raven | Kluger Rabe | 40 / 3 / 0 (Mana: 50\) | skill\_apply\_weakness | Pet\_Debuffer (Hält atk\_down auf dem Ziel) |

## **F) S27: Director AI Events (config/director\_events.json5)**

**Ziel (B2.1):** Definition der dynamischen Events, die das DirectorAISystem (S27) im REALTIME-Modus auslöst.

| Event-ID | Trigger (Bedingung) | Aktion (Was passiert) |
| :---- | :---- | :---- |
| Goblin-Horde | time\_since\_last\_combat \> 120 UND player\_in\_zone("forest") | Spawne 5 goblin\_scout in der Nähe des Spielers. |
| Wandernder Händler | player\_level \> 5 UND random\_chance(0.1) | Spawne npc\_traveling\_merchant auf der Karte. |
| Spider-Infestation | player\_in\_zone("forest\_deep") UND quest\_status("q\_goblin\_plague") \== "COMPLETED" | Spawne spider\_queen an einem vordefinierten Ort. |
| Dwarven-Caravan | reputation\["dwarven\_guild"\] \> 10 UND player\_in\_zone("mountains") | Spawne npc\_dwarven\_merchant (verkauft seltene Erze). |
| Plague-Outbreak | player\_level \== 3 UND player\_in\_zone("startburg") | Aktiviere nurse\_jane Quest-Verfügbarkeit. |

