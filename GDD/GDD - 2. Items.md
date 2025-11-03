# **GDD \- 2\. Items (config/items.json5)**

**Ziel:** Definition aller Item-Stammdaten. Dient als "Datenbank" für den ConfigLoaderService (S1).

## **Glossar (B2.12)**

* **ID:** Die eindeutige Kennung des Items. Wird in opponents.json5, recipes.json5 etc. referenziert.  
* **Slot:** (Bei Ausrüstung) Definiert, wo das Item getragen wird (z.B. WEAPON, HEAD, CHEST).  
* **Stats-Bonus:** (Bei Ausrüstung) Definiert, welche Boni die StatsComponent (S3/S7) erhält.  
* **Effekt:** (Bei Consumables) Definiert, welche Aktion beim Benutzen ausgelöst wird (z.B. Heilung, Statuseffekt).  
* **Max. Stapel:** Wie viele Items dieses Typs auf einem einzigen Inventar-Slot (S7) gestapelt werden können.

## **Syntax-Beispiel (B2.2)**

So wird ein Item in config/items.json5 definiert. Das System (S1) parst dies in ein ItemConfig Pydantic-Modell.

// config/items.json5  
{  
  // 💊 Consumable  
  "potion\_heal\_small": {  
    "name": "Kleiner Heiltrank",  
    "type": "Consumable",  
    "icon\_id": "potion\_red",  
    "effect": { "type": "heal", "amount": 50 },  
    "value\_gold": 5,  
    "max\_stack": 20  
  },  
    
  // ⚔️ Weapon  
  "iron\_sword": {  
    "name": "Eisenschwert",  
    "type": "Equipment",  
    "icon\_id": "sword\_1h",  
    "slot": "WEAPON",  
    "stats\_bonus": { "atk": 5 },  
    "value\_gold": 25,  
    "max\_stack": 1  
  },  
    
  // 🌿 Resource  
  "iron\_ore": {  
    "name": "Eisenerz",  
    "type": "Resource",  
    "icon\_id": "ore\_iron",  
    "value\_gold": 2,  
    "max\_stack": 99  
  }  
}

## **A) 💊 Consumables (Verbrauchsgegenstände)**

| ID | Name | Effekt | Basiswert (Gold) | Max. Stapel |
| :---- | :---- | :---- | :---- | :---- |
| **Tränke (Tier 1\)** |  |  |  |  |
| potion\_heal\_small | Kleiner Heiltrank | {"type": "heal", "amount": 50} | 5 | 20 |
| potion\_mana\_small | Kleiner Manatrank | {"type": "restore\_mana", "amount": 30} | 5 | 20 |
| antidote | Gegengift | {"type": "remove\_effect", "effect\_id": "poison"} | 8 | 20 |
| **Tränke (Tier 2\)** |  |  |  |  |
| potion\_heal\_medium | Mittlerer Heiltrank | {"type": "heal", "amount": 150} | 20 | 20 |
| potion\_mana\_medium | Mittlerer Manatrank | {"type": "restore\_mana", "amount": 75} | 20 | 20 |
| potion\_strength | Stärketrank | {"type": "apply\_effect\_self", "status\_effekt\_id": "atk\_up"} | 30 | 10 |
| potion\_ironhide | Eisenhauttrank | {"type": "apply\_effect\_self", "status\_effekt\_id": "def\_up"} | 30 | 10 |
| potion\_swiftness | Trank der Schnelligkeit | {"type": "apply\_effect\_self", "status\_effekt\_id": "speed\_up"} | 30 | 10 |
| thawing\_potion | Auftau-Trank | {"type": "remove\_effect", "effect\_id": "slow"} | 25 | 20 |
| **Tränke (Tier 3\)** |  |  |  |  |
| potion\_heal\_large | Großer Heiltrank | {"type": "heal", "amount": 400} | 75 | 20 |
| potion\_invisibility | Unsichtbarkeitstrank | {"type": "apply\_effect\_self", "status\_effekt\_id": "invisible"} | 100 | 5 |
| purifying\_elixir | Elixier der Reinigung | {"type": "remove\_effect", "effect\_id": "ALL\_DEBUFFS"} | 120 | 10 |
| **Tränke (Tier 4\)** |  |  |  |  |
| potion\_heal\_superior | Überlegener Heiltrank | {"type": "heal", "amount": 1000} | 250 | 20 |
| potion\_mana\_large | Großer Manatrank | {"type": "restore\_mana", "amount": 200} | 180 | 20 |
| elixir\_of\_giants\_strength | Elixier der Riesenstärke | {"type": "apply\_effect\_self", "status\_effekt\_id": "atk\_up\_major"} | 300 | 5 |
| **Offensiv / Utility** |  |  |  |  |
| bomb\_crude | Rohbombe | {"type": "damage\_aoe", "amount": 50, "damage\_type": "Fire"} | 20 | 20 |
| bomb\_iron | Eisenbombe | {"type": "damage\_aoe", "amount": 150, "damage\_type": "Fire"} | 60 | 20 |
| trap\_snare | Fangeisen | {"type": "apply\_effect\_aoe", "target": "ENEMIES", ...} | 40 | 20 |
| scroll\_fireball | Schriftrolle: Feuerball | {"type": "cast\_skill", "skill\_id": "skill\_fireball"} | 50 | 10 |
| scroll\_teleport\_town | Schriftrolle: Stadtrückkehr | {"type": "teleport", "location": "Startburg"} | 100 | 5 |

## **B) 🌿 Resources (Ressourcen)**

| ID | Name | Basiswert (Gold) | Max. Stapel |
| :---- | :---- | :---- | :---- |
| **Tier 1 (Häufig)** |  |  |  |
| red\_herb | Rotes Kraut | 1 | 99 |
| blue\_herb | Blaues Kraut | 1 | 99 |
| vial | Leere Phiole | 1 | 99 |
| scrap\_leather | Lederreste | 2 | 99 |
| linen\_cloth | Leinenstoff | 2 | 99 |
| iron\_ore | Eisenerz | 2 | 99 |
| coal | Kohle | 1 | 99 |
| **Tier 2 (Ungewöhnlich)** |  |  |  |
| ectoplasm | Ektoplasma | 5 | 99 |
| shadow\_silk | Schattenseide | 6 | 99 |
| obsidian\_shard | Obsidiansplitter | 8 | 99 |
| wyvern\_scale | Wyvernschuppe | 7 | 99 |
| harpy\_feather | Harpyienfeder | 5 | 99 |
| troll\_blood | Trollblut | 10 | 99 |
| steel\_ingot | Stahlbarren | 8 | 99 |
| **Tier 3 (Selten)** |  |  |  |
| mithril\_ore | Mithrilerz | 20 | 99 |
| ancient\_core | Antiker Kern | 30 | 50 |
| lich\_phylactery\_shard | Lich-Phylakterium-Splitter | 35 | 50 |
| manticore\_venom | Mantikor-Gift | 25 | 50 |
| shadow\_leather | Schattenleder | 15 | 99 |
| rune\_thread | Runenfaden | 12 | 99 |
| **Tier 4 (Episch / Legendär)** |  |  |  |
| dragonscale\_red | Rote Drachenschuppe | 100 | 20 |
| void\_crystal | Leerenkristall | 120 | 20 |
| phoenix\_ash | Phönixasche | 150 | 20 |
| star\_metal\_ore | Sternenmetall-Erz | 80 | 50 |
| celestial\_cloth | Himmlischer Stoff | 70 | 50 |

## **C) ⚔️ Weapons (Waffen)**

Ausrüstung ist nicht stapelbar (Max. Stapel \= 1).

| ID | Name | Slot | Stats-Bonus | Basiswert (Gold) | Max. Stapel |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Tier 1 (Eisen/Holz)** |  |  |  |  |  |
| iron\_sword | Eisenschwert | WEAPON | {"atk": 5} | 25 | 1 |
| iron\_dagger | Eisendolch | WEAPON | {"atk": 3, "speed": 2} | 20 | 1 |
| iron\_axe | Eisenaxt | WEAPON | {"atk": 6, "speed": \-1} | 28 | 1 |
| iron\_mace | Eisenstreitkolben | WEAPON | {"atk": 7, "speed": \-2} | 30 | 1 |
| short\_spear | Kurzer Speer | WEAPON | {"atk": 4, "speed": 1} | 22 | 1 |
| hunting\_bow | Jagdbogen | WEAPON (TWO\_HAND) | {"atk": 4} | 25 | 1 |
| oaken\_staff | Eichenstab | WEAPON (TWO\_HAND) | {"magic\_atk": 5, ...} | 30 | 1 |
| **Tier 2 (Stahl/Magisch)** |  |  |  |  |  |
| steel\_sword | Stahlschwert | WEAPON | {"atk": 10} | 120 | 1 |
| steel\_greatsword | Stahl-Großschwert | WEAPON (TWO\_HAND) | {"atk": 12, ...} | 150 | 1 |
| orcish\_battleaxe | Orkische Streitaxt | WEAPON (TWO\_HAND) | {"atk": 14, ...} | 160 | 1 |
| elven\_bow | Elfenbogen | WEAPON (TWO\_HAND) | {"atk": 8, "speed": 3} | 140 | 1 |
| apprentice\_staff | Lehrlingsstab | WEAPON (TWO\_HAND) | {"magic\_atk": 12, ...} | 150 | 1 |
| obsidian\_dagger | Obsidiandolch | WEAPON | {"atk": 5, "magic\_atk": 8} | 180 | 1 |
| **Tier 3 (Elite/Mithril)** |  |  |  |  |  |
| mithril\_sword | Mithrilschwert | WEAPON | {"atk": 15, "speed": 2} | 450 | 1 |
| golem\_core\_hammer | Golemkern-Hammer | WEAPON (TWO\_HAND) | {"atk": 18, ...} | 500 | 1 |
| dread\_knight\_sword | Schwert des Schreckensritters | WEAPON | {"atk": 15, "lifesteal": ...} | 700 | 1 |
| archmage\_staff | Erzmagier-Stab | WEAPON (TWO\_HAND) | {"magic\_atk": 30, ...} | 750 | 1 |
| harpy\_queen\_dagger | Dolch der Harpyienkönigin | WEAPON | {"atk": 12, "speed": 5} | 650 | 1 |
| **Tier 4 (Legendär)** |  |  |  |  |  |
| phoenix\_blade | Phönixklinge | WEAPON | {"atk": 20, ...} | 2000 | 1 |
| starmetal\_greatsword | Sternenmetall-Großschwert | WEAPON (TWO\_HAND) | {"atk": 25, ...} | 2500 | 1 |
| staff\_of\_the\_lich\_king | Stab des Lichkönigs | WEAPON (TWO\_HAND) | {"magic\_atk": 40, ...} | 2800 | 1 |

## **D) 🛡️ Armor (Rüstung)**

| ID | Name | Slot | Stats-Bonus | Basiswert (Gold) | Max. Stapel |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Tier 1: Sets (Level 1-10)** |  |  |  |  |  |
| armor\_iron\_helmet | Eisenhelm | HEAD | {"def": 5, ...} | 20 | 1 |
| armor\_iron\_plate | Eisenharnisch | CHEST | {"def": 8, ...} | 40 | 1 |
| armor\_iron\_gauntlets | Eisenhandschuhe | HANDS | {"def": 3} | 15 | 1 |
| armor\_iron\_boots | Eisenstiefel | FEET | {"def": 3, ...} | 15 | 1 |
| armor\_leather\_cap | Lederkappe | HEAD | {"def": 2} | 12 | 1 |
| armor\_leather\_tunic | Ledertunika | CHEST | {"def": 5, ...} | 25 | 1 |
| armor\_leather\_gloves | Lederhandschuhe | HANDS | {"def": 1} | 8 | 1 |
| armor\_leather\_boots | Lederstiefel | FEET | {"def": 1, ...} | 8 | 1 |
| armor\_mage\_hood | Magierkapuze | HEAD | {"def": 1, ...} | 15 | 1 |
| armor\_mage\_robe | Magierrobe | CHEST | {"def": 3, ...} | 30 | 1 |
| armor\_mage\_gloves | Magierhandschuhe | HANDS | {"magic\_atk": 2} | 10 | 1 |
| armor\_mage\_sandals | Magiersandalen | FEET | {"def": 1, ...} | 10 | 1 |
| **Tier 2: Sets (Level 10-20)** |  |  |  |  |  |
| armor\_steel\_helmet | Stahlhelm | HEAD | {"def": 8, ...} | 80 | 1 |
| armor\_steel\_plate | Stahlharnisch | CHEST | {"def": 12, ...} | 140 | 1 |
| armor\_steel\_gauntlets | Stahlhandschuhe | HANDS | {"def": 5} | 60 | 1 |
| armor\_steel\_boots | Stahlstiefel | FEET | {"def": 5, ...} | 60 | 1 |
| armor\_hardleather\_cap | Gehärtete Lederkappe | HEAD | {"def": 4, ...} | 70 | 1 |
| armor\_hardleather\_tunic | Gehärtete Ledertunika | CHEST | {"def": 8, ...} | 130 | 1 |
| armor\_hardleather\_gloves | Gehärtete Lederhandschuhe | HANDS | {"def": 3, ...} | 55 | 1 |
| armor\_hardleather\_boots | Gehärtete Lederstiefel | FEET | {"def": 3, ...} | 55 | 1 |
| armor\_silk\_hood | Seidenkapuze | HEAD | {"def": 2, ...} | 75 | 1 |
| armor\_silk\_robe | Seidenrobe | CHEST | {"def": 5, ...} | 135 | 1 |
| armor\_silk\_gloves | Seidenhandschuhe | HANDS | {"def": 1, ...} | 58 | 1 |
| armor\_silk\_boots | Seidenstiefel | FEET | {"def": 1, ...} | 58 | 1 |
| **Tier 3: Sets (Level 20-30)** |  |  |  |  |  |
| armor\_mithril\_helmet | Mithrilhelm | HEAD | {"def": 12, ...} | 300 | 1 |
| armor\_mithril\_plate | Mithrilharnisch | CHEST | {"def": 18, ...} | 500 | 1 |
| armor\_mithril\_gauntlets | Mithrilhandschuhe | HANDS | {"def": 9, ...} | 220 | 1 |
| armor\_mithril\_boots | Mithrilstiefel | FEET | {"def": 9, ...} | 220 | 1 |
| armor\_shadow\_cowl | Schattenkapuze | HEAD | {"def": 6, ...} | 280 | 1 |
| armor\_shadow\_tunic | Schattentunika | CHEST | {"def": 12, ...} | 480 | 1 |
| armor\_shadow\_gloves | Schattenhandschuhe | HANDS | {"def": 4, ...} | 210 | 1 |
| armor\_shadow\_boots | Schattenstiefel | FEET | {"def": 4, ...} | 210 | 1 |
| armor\_arcanist\_hood | Arkanistenkapuze | HEAD | {"def": 4, ...} | 290 | 1 |
| armor\_arcanist\_robe | Arkanistenrobe | CHEST | {"def": 8, ...} | 490 | 1 |
| armor\_arcanist\_gloves | Arkanistenhandschuhe | HANDS | {"def": 2, ...} | 215 | 1 |
| armor\_arcanist\_boots | Arkanistenstiefel | FEET | {"def": 2, ...} | 215 | 1 |
| **Spezial-Rüstung / Schilde** |  |  |  |  |  |
| iron\_shield | Eisenschild | SHIELD | {"def": 5} | 30 | 1 |
| steel\_shield | Stahlschild | SHIELD | {"def": 10} | 110 | 1 |
| obsidian\_shield | Obsidianschild | SHIELD | {"def": 7, ...} | 150 | 1 |
| mithril\_shield | Mithrilschild | SHIELD | {"def": 15, ...} | 400 | 1 |
| dragonscale\_shield | Drachenschuppen-Schild | SHIELD | {"def": 25, ...} | 1500 | 1 |
| spider\_silk\_robe | Spinnenseidenrobe | CHEST | {"def": 4, ...} | 200 | 1 |

## **E) 💍 Accessoires**

| ID | Name | Slot | Stats-Bonus | Basiswert (Gold) | Max. Stapel |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Tier 1** |  |  |  |  |  |
| ring\_of\_health\_small | Kleiner Gesundheitsring | RING | {"max\_hp": 25} | 40 | 1 |
| ring\_of\_mana\_small | Kleiner Manaring | RING | {"max\_mana": 25} | 40 | 1 |
| ring\_of\_strength\_small | Kleiner Ring der Stärke | RING | {"atk": 1} | 35 | 1 |
| ring\_of\_protection\_small | Kleiner Schutzring | RING | {"def": 1} | 35 | 1 |
| amulet\_of\_apprentice | Amulett des Lehrlings | AMULET | {"magic\_atk": 2} | 45 | 1 |
| **Tier 2** |  |  |  |  |  |
| ring\_of\_health\_medium | Mittlerer Gesundheitsring | RING | {"max\_hp": 75} | 120 | 1 |
| ring\_of\_mana\_medium | Mittlerer Manaring | RING | {"max\_mana": 50} | 120 | 1 |
| ring\_of\_strength | Ring der Stärke | RING | {"atk": 3} | 110 | 1 |
| ring\_of\_protection | Ring des Schutzes | RING | {"def": 3} | 110 | 1 |
| ring\_of\_speed | Ring der Geschwindigkeit | RING | {"speed": 3} | 130 | 1 |
| amulet\_of\_the\_trapper | Amulett des Fallenstellers | AMULET | {"skill\_bonus": ...} | 150 | 1 |
| amulet\_of\_the\_pyromancer | Amulett des Pyromanen | AMULET | {"fire\_damage...": 10} | 150 | 1 |
| amulet\_of\_the\_golem | Amulett des Golems | AMULET | {"max\_hp": 100, ...} | 180 | 1 |
| janes\_worn\_amulet | Janes getragenes Amulett | AMULET | {"magic\_resist": 5} | 50 | 1 |
| **Tier 3** |  |  |  |  |  |
| ring\_of\_the\_vampire | Ring des Vampirs | RING | {"lifesteal": 0.03} | 500 | 1 |
| ring\_of\_the\_archmage | Ring des Erzmagiers | RING | {"magic\_atk": 5, ...} | 450 | 1 |
| ring\_of\_the\_berserker | Ring des Berserkers | RING | {"atk": 5, "def": \-3} | 400 | 1 |
| amulet\_of\_the\_lich | Amulett des Lichs | AMULET | {"magic\_resist": 15, ...} | 800 | 1 |

## **F) 📜 Quest Items (Questgegenstände)**

Quest-Items können nicht verkauft oder gestapelt werden.

| ID | Name | Typ | Basiswert (Gold) | Max. Stapel |
| :---- | :---- | :---- | :---- | :---- |
| janes\_lost\_amulet | Janes verlorenes Amulett | Quest | 0 | 1 |
| guard\_report | Wach-Bericht | Quest | 0 | 1 |
| orc\_warchief\_banner | Banner des Ork-Häuptlings | Quest | 0 | 1 |
| spider\_queen\_venom\_gland | Giftblase der Spinnenkönigin | Quest | 0 | 1 |
| boris\_tools\_delivery | Boris' Werkzeuglieferung | Quest | 0 | 1 |
| lich\_phylactery\_fragment | Fragment des Lich-Phylakteriums | Quest | 0 | 1 |

## **G) 💰 Trade Goods (Handelswaren \- Plunder)**

| ID | Name | Typ | Basiswert (Gold) | Max. Stapel |
| :---- | :---- | :---- | :---- | :---- |
| wolf\_pelt | Wolfspelz | Trade Good | 5 | 50 |
| goblin\_ear | Goblin-Ohr | Trade Good | 2 | 99 |
| broken\_sword\_hilt | Zerbrochener Schwertgriff | Trade Good | 1 | 50 |
| chipped\_gemstone | Abgeschlagener Edelstein | Trade Good | 8 | 50 |
| orcish\_tusk | Ork-Hauer | Trade Good | 12 | 50 |
| faded\_scroll | Verblasste Schriftrolle | Trade Good | 1 | 50 |
| dull\_crystal | Trüber Kristall | Trade Good | 10 | 50 |
| silver\_ring | Silberring | Trade Good | 25 | 20 |
| gold\_goblet | Goldener Kelch | Trade Good | 100 | 5 |

## **H) 📐 Schematics (Baupläne & Rezepte)**

Baupläne sind einzigartig (Max. Stapel \= 1).

| ID | Name | Beruf | Basiswert (Gold) | Max. Stapel |
| :---- | :---- | :---- | :---- | :---- |
| **Schmiedekunst (Tier 1\)** |  |  |  |  |
| blueprint\_iron\_plate | Bauplan: Eisenharnisch | Schmiedekunst | 20 | 1 |
| blueprint\_iron\_sword | Bauplan: Eisenschwert | Schmiedekunst | 15 | 1 |
| blueprint\_iron\_axe | Bauplan: Eisenaxt | Schmiedekunst | 15 | 1 |
| blueprint\_iron\_mace | Bauplan: Eisenstreitkolben | Schmiedekunst | 15 | 1 |
| blueprint\_iron\_dagger | Bauplan: Eisendolch | Schmiedekunst | 15 | 1 |
| blueprint\_iron\_shield | Bauplan: Eisenschild | Schmiedekunst | 15 | 1 |
| blueprint\_hunting\_bow | Bauplan: Jagdbogen | Schmiedekunst | 15 | 1 |
| **Schmiedekunst (Tier 2\)** |  |  |  |  |
| blueprint\_steel\_plate | Bauplan: Stahlharnisch | Schmiedekunst | 80 | 1 |
| blueprint\_steel\_sword | Bauplan: Stahlschwert | Schmiedekunst | 70 | 1 |
| blueprint\_steel\_greatsword | Schema: Stahl-Großschwert | Schmiedekunst | 90 | 1 |
| blueprint\_elven\_bow | Design: Elfenbogen | Schmiedekunst | 100 | 1 |
| blueprint\_obsidian\_dagger | Design: Obsidiandolch | Schmiedekunst | 120 | 1 |
| **Schmiedekunst (Tier 3\)** |  |  |  |  |
| design\_mithril\_sword | Design: Mithrilschwert | Schmiedekunst | 300 | 1 |
| design\_mithril\_plate | Design: Mithrilharnisch | Schmiedekunst | 350 | 1 |
| design\_golem\_core\_hammer | Design: Golemkern-Hammer | Schmiedekunst | 400 | 1 |
| **Alchemie (Tier 1\)** |  |  |  |  |
| recipe\_heal\_small | Rezept: Kleiner Heiltrank | Alchemie | 5 | 1 |
| recipe\_mana\_small | Rezept: Kleiner Manatrank | Alchemie | 5 | 1 |
| recipe\_antidote | Rezept: Gegengift | Alchemie | 10 | 1 |
| **Alchemie (Tier 2\)** |  |  |  |  |
| recipe\_heal\_medium | Rezept: Mittlerer Heiltrank | Alchemie | 40 | 1 |
| recipe\_mana\_medium | Rezept: Mittlerer Manatrank | Alchemie | 40 | 1 |
| recipe\_strength\_potion | Formel: Stärketrank | Alchemie | 50 | 1 |
| recipe\_ironhide\_potion | Formel: Eisenhauttrank | Alchemie | 50 | 1 |
| recipe\_swiftness\_potion | Formel: Trank der Schnelligkeit | Alchemie | 50 | 1 |
| recipe\_crude\_bomb | Formel: Rohbombe | Alchemie | 60 | 1 |
| **AlchemIE (Tier 3\)** |  |  |  |  |
| recipe\_heal\_large | Formel: Großer Heiltrank | Alchemie | 150 | 1 |
| recipe\_invisibility\_potion | Formel: Unsichtbarkeitstrank | Alchemie | 200 | 1 |
| recipe\_purifying\_elixir | Formel: Elixier der Reinigung | Alchemie | 220 | 1 |
| **Schneiderei (Tier 1\)** |  |  |  |  |
| pattern\_leather\_cap | Schnittmuster: Lederkappe | Schneiderei | 10 | 1 |
| pattern\_leather\_tunic | Schnittmuster: Ledertunika | Schneiderei | 15 | 1 |
| pattern\_mage\_hood | Schnittmuster: Magierkapuze | Schneiderei | 10 | 1 |
| pattern\_mage\_robe | Schnittmuster: Magierrobe | Schneiderei | 15 | 1 |
| pattern\_oaken\_staff | Bauplan: Eichenstab | Schneiderei | 20 | 1 |
| **Schneiderei (Tier 2\)** |  |  |  |  |
| pattern\_hardleather\_cap | Schnittmuster: Geh. Lederkappe | Schneiderei | 60 | 1 |
| pattern\_hardleather\_tunic | Schnittmuster: Geh. Ledertunika | Schneiderei | 80 | 1 |
| pattern\_silk\_hood | Schnittmuster: Seidenkapuze | Schneiderei | 65 | 1 |
| pattern\_silk\_robe | Schnittmuster: Seidenrobe | Schneiderei | 85 | 1 |
| pattern\_apprentice\_staff | Bauplan: Lehrlingsstab | Schneiderei | 100 | 1 |
| **Schneiderei (Tier 3\)** |  |  |  |  |
| pattern\_shadow\_cowl | Schnittmuster: Schattenkapuze | Schneiderei | 300 | 1 |
| pattern\_shadow\_tunic | Schnittmuster: Schattentunika | Schneiderei | 350 | 1 |
| pattern\_arcanist\_hood | Schnittmuster: Arkanistenkapuze | Schneiderei | 310 | 1 |
| pattern\_arcanist\_robe | Schnittmuster: Arkanistenrobe | Schneiderei | 360 | 1 |
| pattern\_archmage\_staff | Bauplan: Erzmagier-Stab | Schneiderei | 400 | 1 |

