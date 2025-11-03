# **GDD \- 5\. Berufe & Rezepte v2 (Überarbeitet)**

**Ziel (B2.1):** Definition aller Handwerksberufe und der dazugehörigen Rezepte. Dient als "Stückliste" (Bill of Materials) für den CraftingService (S10b).

## **Glossar (B2.12)**

* **Beruf:** Eine Handwerks-Fähigkeit (z.B. Schmiedekunst), die gelevelt werden kann.  
* **Rezept:** Eine Anleitung zur Herstellung eines Items.  
* **Station:** Der Ort, an dem gecraftet werden muss (z.B. Schmiede).  
* **Benötigter Skill:** Das Level, das der Beruf haben muss, um das Rezept *ausführen* zu können.  
* **Freischaltung (B2.8):** Das Item (Bauplan/Rezept aus GDD-2), das der Spieler konsumieren muss, um das Rezept *zu lernen*.

## **A) S10b: Handwerksberufe (Crafting)**

Wir definieren 3 primäre Herstellungsberufe:

* **Schmiedekunst:** Stellt schwere Rüstungen (Eisen, Stahl, Mithril) und alle Metallwaffen (Schwerter, Äxte, Dolche, Bögen) her.  
* **Schneiderei:** Stellt leichte (Stoff) und mittlere (Leder) Rüstungen her, sowie magische Waffen (Stäbe).  
* **Alchemie:** Stellt Tränke, Elixiere und Bomben her.

### **Handwerks-Stationen**

* **Schmiede (Forge):** Wird für alle Schmiedekunst-Rezepte benötigt.  
* **Werkbank (Workbench):** Wird für alle Schneiderei-Rezepte benötigt.  
* **Alchemielabor (Alchemy Lab):** Wird für alle Alchemie-Rezepte benötigt.

## **Syntax-Beispiel (B2.2)**

So wird ein Rezept in config/recipes.json5 definiert.

// config/recipes.json5  
{  
  "iron\_sword": {  
    "output\_id": "iron\_sword",  
    "output\_name": "Eisenschwert",  
    "output\_quantity": 1,  
    "profession": "Schmiedekunst",  
    "skill\_level\_required": 1,  
    "station\_required": "Schmiede",  
      
    // B2.8: Definiert, welches Item das Rezept freischaltet  
    "unlocked\_by\_item": "blueprint\_iron\_sword",   
      
    // Die Stückliste  
    "ingredients": \[  
      { "item\_id": "iron\_ore", "quantity": 5 },  
      { "item\_id": "scrap\_leather", "quantity": 2 }  
    \]  
  },  
  "potion\_heal\_small": {  
    "output\_id": "potion\_heal\_small",  
    "output\_name": "Kleiner Heiltrank",  
    "output\_quantity": 1,  
    "profession": "Alchemie",  
    "skill\_level\_required": 1,  
    "station\_required": "Alchemielabor",  
    "unlocked\_by\_item": "recipe\_heal\_small",  
    "ingredients": \[  
      { "item\_id": "red\_herb", "quantity": 2 },  
      { "item\_id": "vial", "quantity": 1 }  
    \]  
  }  
}

## **B) Rezept-Liste (config/recipes.json5)**

### **1\. ⚔️ Rezepte: Schmiedekunst**

| Output (ID) | Name | Menge | Benötigter Skill | Station | Benötigte Materialien (Stückliste) | Freischaltung (B2.8) |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Tier 1 (Skill 1-25)** |  |  |  |  |  |  |
| steel\_ingot | Stahlbarren | 1 | 1 | Schmiede | {"iron\_ore": 2, "coal": 1} | (Standardrezept) |
| iron\_sword | Eisenschwert | 1 | 1 | Schmiede | {"iron\_ore": 5, "scrap\_leather": 2} | blueprint\_iron\_sword |
| iron\_axe | Eisenaxt | 1 | 5 | Schmiede | {"iron\_ore": 6, "scrap\_leather": 1} | blueprint\_iron\_axe |
| iron\_mace | Eisenstreitkolben | 1 | 5 | Schmiede | {"iron\_ore": 7} | blueprint\_iron\_mace |
| iron\_dagger | Eisendolch | 1 | 1 | Schmiede | {"iron\_ore": 3, "scrap\_leather": 1} | blueprint\_iron\_dagger |
| iron\_shield | Eisenschild | 1 | 10 | Schmiede | {"iron\_ore": 8} | blueprint\_iron\_shield |
| hunting\_bow | Jagdbogen | 1 | 10 | Schmiede | {"iron\_ore": 4, "scrap\_leather": 4} | blueprint\_hunting\_bow |
| armor\_iron\_helmet | Eisenhelm | 1 | 15 | Schmiede | {"iron\_ore": 6} | (Standardrezept Tier 1\) |
| armor\_iron\_plate | Eisenharnisch | 1 | 20 | Schmiede | {"iron\_ore": 10} | blueprint\_iron\_plate |
| armor\_iron\_gauntlets | Eisenhandschuhe | 1 | 10 | Schmiede | {"iron\_ore": 4} | (Standardrezept Tier 1\) |
| armor\_iron\_boots | Eisenstiefel | 1 | 10 | Schmiede | {"iron\_ore": 4} | (Standardrezept Tier 1\) |
| **Tier 2 (Skill 25-50)** |  |  |  |  |  |  |
| steel\_sword | Stahlschwert | 1 | 25 | Schmiede | {"steel\_ingot": 8, "scrap\_leather": 3} | blueprint\_steel\_sword |
| steel\_greatsword | Stahl-Großschwert | 1 | 30 | Schmiede | {"steel\_ingot": 12, "scrap\_leather": 4} | blueprint\_steel\_greatsword |
| orcish\_battleaxe | Orkische Streitaxt | 1 | 35 | Schmiede | {"steel\_ingot": 10, "orcish\_tusk": 1} | blueprint\_orcish\_battleaxe |
| elven\_bow | Elfenbogen | 1 | 35 | Schmiede | {"steel\_ingot": 5, "shadow\_silk": 3} | blueprint\_elven\_bow |
| obsidian\_dagger | Obsidiandolch | 1 | 40 | Schmiede | {"obsidian\_shard": 5, "steel\_ingot": 2} | blueprint\_obsidian\_dagger |
| steel\_shield | Stahlschild | 1 | 25 | Schmiede | {"steel\_ingot": 6} | (Standardrezept Tier 2\) |
| armor\_steel\_helmet | Stahlhelm | 1 | 30 | Schmiede | {"steel\_ingot": 7} | (Standardrezept Tier 2\) |
| armor\_steel\_plate | Stahlharnisch | 1 | 40 | Schmiede | {"steel\_ingot": 12} | blueprint\_steel\_plate |
| armor\_steel\_gauntlets | Stahlhandschuhe | 1 | 25 | Schmiede | {"steel\_ingot": 5} | (Standardrezept Tier 2\) |
| armor\_steel\_boots | Stahlstiefel | 1 | 25 | Schmiede | {"steel\_ingot": 5} | (Standardrezept Tier 2\) |
| **Tier 3 (Skill 50-75)** |  |  |  |  |  |  |
| mithril\_ingot | Mithrilbarren | 1 | 50 | Schmiede | {"mithril\_ore": 2, "coal": 2} | (Standardrezept Tier 3\) |
| mithril\_sword | Mithrilschwert | 1 | 50 | Schmiede | {"mithril\_ingot": 8, "shadow\_leather": 2} | design\_mithril\_sword |
| golem\_core\_hammer | Golemkern-Hammer | 1 | 60 | Schmiede | {"mithril\_ingot": 10, "ancient\_core": 1} | design\_golem\_core\_hammer |
| mithril\_shield | Mithrilschild | 1 | 50 | Schmiede | {"mithril\_ingot": 7} | (Standardrezept Tier 3\) |
| armor\_mithril\_helmet | Mithrilhelm | 1 | 55 | Schmiede | {"mithril\_ingot": 8} | (Standardrezept Tier 3\) |
| armor\_mithril\_plate | Mithrilharnisch | 1 | 65 | Schmiede | {"mithril\_ingot": 14} | design\_mithril\_plate |
| armor\_mithril\_gauntlets | Mithrilhandschuhe | 1 | 50 | Schmiede | {"mithril\_ingot": 6} | (Standardrezept Tier 3\) |
| armor\_mithril\_boots | Mithrilstiefel | 1 | 50 | Schmiede | {"mithril\_ingot": 6} | (Standardrezept Tier 3\) |

### **2\. 🧵 Rezepte: Schneiderei**

| Output (ID) | Name | Menge | Benötigter Skill | Station | Benötigte Materialien (Stückliste) | Freischaltung (B2.8) |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Tier 1 (Skill 1-25)** |  |  |  |  |  |  |
| armor\_leather\_cap | Lederkappe | 1 | 1 | Werkbank | {"scrap\_leather": 4} | pattern\_leather\_cap |
| armor\_leather\_tunic | Ledertunika | 1 | 5 | Werkbank | {"scrap\_leather": 8} | pattern\_leather\_tunic |
| armor\_leather\_gloves | Lederhandschuhe | 1 | 1 | Werkbank | {"scrap\_leather": 3} | (Standardrezept Tier 1\) |
| armor\_leather\_boots | Lederstiefel | 1 | 1 | Werkbank | {"scrap\_leather": 3} | (Standardrezept Tier 1\) |
| armor\_mage\_hood | Magierkapuze | 1 | 1 | Werkbank | {"linen\_cloth": 4} | pattern\_mage\_hood |
| armor\_mage\_robe | Magierrobe | 1 | 5 | Werkbank | {"linen\_cloth": 8} | pattern\_mage\_robe |
| armor\_mage\_gloves | Magierhandschuhe | 1 | 1 | Werkbank | {"linen\_cloth": 3} | (Standardrezept Tier 1\) |
| armor\_mage\_sandals | Magiersandalen | 1 | 1 | Werkbank | {"linen\_cloth": 3} | (Standardrezept Tier 1\) |
| oaken\_staff | Eichenstab | 1 | 10 | Werkbank | {"linen\_cloth": 5, "iron\_ore": 2} | pattern\_oaken\_staff |
| **Tier 2 (Skill 25-50)** |  |  |  |  |  |  |
| hardened\_leather | Gehärtetes Leder | 1 | 25 | Werkbank | {"scrap\_leather": 5, "coal": 1} | (Standardrezept Tier 2\) |
| silk\_bolt | Seidenballe | 1 | 25 | Werkbank | {"shadow\_silk": 5} | (Standardrezept Tier 2\) |
| armor\_hardleather\_cap | Geh. Lederkappe | 1 | 30 | Werkbank | {"hardened\_leather": 4, "shadow\_silk": 1} | pattern\_hardleather\_cap |
| armor\_hardleather\_tunic | Geh. Ledertunika | 1 | 35 | Werkbank | {"hardened\_leather": 8, "shadow\_silk": 2} | pattern\_hardleather\_tunic |
| armor\_hardleather\_gloves | Geh. Lederhandschuhe | 1 | 25 | Werkbank | {"hardened\_leather": 3} | (Standardrezept Tier 2\) |
| armor\_hardleather\_boots | Geh. Lederstiefel | 1 | 25 | Werkbank | {"hardened\_leather": 3} | (Standardrezept Tier 2\) |
| armor\_silk\_hood | Seidenkapuze | 1 | 30 | Werkbank | {"silk\_bolt": 4, "ectoplasm": 1} | pattern\_silk\_hood |
| armor\_silk\_robe | Seidenrobe | 1 | 35 | Werkbank | {"silk\_bolt": 8, "ectoplasm": 2} | pattern\_silk\_robe |
| armor\_silk\_gloves | Seidenhandschuhe | 1 | 25 | Werkbank | {"silk\_bolt": 3} | (Standardrezept Tier 2\) |
| armor\_silk\_boots | Seidenstiefel | 1 | 25 | Werkbank | {"silk\_bolt": 3} | (Standardrezept Tier 2\) |
| apprentice\_staff | Lehrlingsstab | 1 | 40 | Werkbank | {"silk\_bolt": 5, "obsidian\_shard": 3} | pattern\_apprentice\_staff |
| spider\_silk\_robe | Spinnenseidenrobe | 1 | 45 | Werkbank | {"silk\_bolt": 10, "manticore\_venom": 1} | pattern\_spider\_silk\_robe |
| **Tier 3 (Skill 50-75)** |  |  |  |  |  |  |
| shadow\_weave | Schattengewebe | 1 | 50 | Werkbank | {"silk\_bolt": 2, "ectoplasm": 2} | (Standardrezept Tier 3\) |
| rune\_leather | Runenleder | 1 | 50 | Werkbank | {"hardened\_leather": 2, "rune\_thread": 1} | (Standardrezept Tier 3\) |
| armor\_shadow\_cowl | Schattenkapuze | 1 | 55 | Werkbank | {"rune\_leather": 5, "shadow\_weave": 2} | pattern\_shadow\_cowl |
| armor\_shadow\_tunic | Schattentunika | 1 | 60 | Werkbank | {"rune\_leather": 10, "shadow\_weave": 4} | pattern\_shadow\_tunic |
| armor\_shadow\_gloves | Schattenhandschuhe | 1 | 50 | Werkbank | {"rune\_leather": 4} | (Standardrezept Tier 3\) |
| armor\_shadow\_boots | Schattenstiefel | 1 | 50 | Werkbank | {"rune\_leather": 4} | (Standardrezept Tier 3\) |
| armor\_arcanist\_hood | Arkanistenkapuze | 1 | 55 | Werkbank | {"shadow\_weave": 5, "rune\_thread": 2} | pattern\_arcanist\_hood |
| armor\_arcanist\_robe | Arkanistenrobe | 1 | 60 | Werkbank | {"shadow\_weave": 10, "rune\_thread": 4} | pattern\_arcanist\_robe |
| armor\_arcanist\_gloves | Arkanistenhandschuhe | 1 | 50 | Werkbank | {"shadow\_weave": 4} | (Standardrezept Tier 3\) |
| armor\_arcanist\_boots | Arkanistenstiefel | 1 | 50 | Werkbank | {"shadow\_weave": 4} | (Standardrezept Tier 3\) |
| archmage\_staff | Erzmagier-Stab | 1 | 65 | Werkbank | {"shadow\_weave": 8, "ancient\_core": 1} | pattern\_archmage\_staff |

### **3\. ⚗️ Rezepte: Alchemie**

| Output (ID) | Name | Menge | Benötigter Skill | Station | Benötigte Materialien (Stückliste) | Freischaltung (B2.8) |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Tier 1 (Skill 1-25)** |  |  |  |  |  |  |
| potion\_heal\_small | Kleiner Heiltrank | 1 | 1 | Alchemielabor | {"red\_herb": 2, "vial": 1} | recipe\_heal\_small |
| potion\_mana\_small | Kleiner Manatrank | 1 | 1 | Alchemielabor | {"blue\_herb": 2, "vial": 1} | recipe\_mana\_small |
| antidote | Gegengift | 1 | 10 | Alchemielabor | {"red\_herb": 1, "blue\_herb": 1, "vial": 1} | recipe\_antidote |
| thawing\_potion | Auftau-Trank | 1 | 15 | Alchemielabor | {"blue\_herb": 2, "coal": 1, "vial": 1} | (Standardrezept Tier 1\) |
| **Tier 2 (Skill 25-50)** |  |  |  |  |  |  |
| potion\_heal\_medium | Mittlerer Heiltrank | 1 | 25 | Alchemielabor | {"potion\_heal\_small": 2, "troll\_blood": 1} | recipe\_heal\_medium |
| potion\_mana\_medium | Mittlerer Manatrank | 1 | 25 | Alchemielabor | {"potion\_mana\_small": 2, "ectoplasm": 1} | recipe\_mana\_medium |
| potion\_strength | Stärketrank | 1 | 30 | Alchemielabor | {"red\_herb": 3, "orcish\_tusk": 1, "vial": 1} | recipe\_strength\_potion |
| potion\_ironhide | Eisenhauttrank | 1 | 30 | Alchemielabor | {"iron\_ore": 1, "blue\_herb": 2, "vial": 1} | recipe\_ironhide\_potion |
| potion\_swiftness | Trank der Schnelligkeit | 1 | 30 | Alchemielabor | {"blue\_herb": 3, "harpy\_feather": 1, "vial": 1} | recipe\_swiftness\_potion |
| bomb\_crude | Rohbombe | 3 | 35 | Alchemielabor | {"iron\_ore": 1, "coal": 2, "linen\_cloth": 1} | recipe\_crude\_bomb |
| **Tier 3 (Skill 50-75)** |  |  |  |  |  |  |
| potion\_heal\_large | Großer Heiltrank | 1 | 50 | Alchemielabor | {"potion\_heal\_medium": 2, "ancient\_core": 1} | recipe\_heal\_large |
| potion\_invisibility | Unsichtbarkeitstrank | 1 | 55 | Alchemielabor | {"shadow\_silk": 2, "ectoplasm": 2, "vial": 1} | recipe\_invisibility\_potion |
| purifying\_elixir | Elixier der Reinigung | 1 | 60 | Alchemielabor | {"troll\_blood": 1, "manticore\_venom": 1, "vial": 1} | recipe\_purifying\_elixir |
| bomb\_iron | Eisenbombe | 3 | 50 | Alchemielabor | {"bomb\_crude": 3, "steel\_ingot": 1} | (Standardrezept Tier 3\) |
| elixir\_of\_giants\_strength | Elixier der Riesenstärke | 1 | 65 | Alchemielabor | {"potion\_strength": 2, "troll\_blood": 3} | (Standardrezept Tier 3\) |

