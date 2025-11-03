# **GDD \- 6\. Loot-Tabellen & Beute (config/loot\_tables.json5)**

**Ziel (B2.1):** Definition aller Loot-Tabellen. Legt fest, welche Items (GDD-2) von welchen Gegnern (GDD-1) mit welcher Wahrscheinlichkeit fallen gelassen werden.

## **Glossar (B2.12)**

* **Loot-Tabelle:** Eine Liste von "Pools", die einem Gegner zugewiesen ist.  
* **Pool:** Eine Unter-Liste von Items. Das System wählt X Items aus jedem Pool aus.  
* **Garantiert:** Ein Pool, bei dem die Chance 100% ist.  
* **Chance:** Die Wahrscheinlichkeit (0.0 bis 1.0), dass ein Item aus dem Pool ausgewählt wird.  
* **Menge:** Kann eine Zahl (z.B. 1\) oder ein Bereich (z.B. \[1, 5\]) sein.

## **Syntax-Beispiel (B2.2)**

Dies ist das **tatsächliche json5-Format (B2.2)**, das in config/loot\_tables.json5 verwendet wird. Das alte Textformat wird nicht mehr genutzt.

// config/loot\_tables.json5  
{  
  // Wird von base\_goblin (GDD-1) genutzt  
  "lt\_goblin\_base": {  
    "pools": \[  
      {  
        // Pool 1: Garantiert  
        "rolls": 1, // Wähle 1 Item aus diesem Pool  
        "items": \[  
          { "item\_id": "goblin\_ear", "quantity": 1, "chance": 1.0 } // 100%  
        \]  
      },  
      {  
        // Pool 2: Materialien (Wähle 1\)  
        "rolls": 1,  
        "items": \[  
          { "item\_id": "scrap\_leather", "quantity": \[1, 3\], "chance": 0.4 }, // 40% auf 1-3  
          { "item\_id": "linen\_cloth", "quantity": \[1, 2\], "chance": 0.4 },   // 40% auf 1-2  
          { "item\_id": "broken\_sword\_hilt", "quantity": 1, "chance": 0.1 } // 10%  
        \]  
      },  
      {  
        // Pool 3: Selten (Wähle 1\)  
        "rolls": 1,  
        "items": \[  
          { "item\_id": "potion\_heal\_small", "quantity": 1, "chance": 0.05 }, // 5%  
          { "item\_id": "blueprint\_iron\_dagger", "quantity": 1, "chance": 0.01 } // 1%  
        \]  
      }  
    \]  
  },  
    
  // Wird von bandit\_thug (GDD-1) genutzt, wenn Quest q\_lost\_amulet aktiv ist  
  "lt\_bandit\_quest\_amulet": {  
    "condition\_quest\_active": "q\_lost\_amulet", // Diese Tabelle wird nur bei aktiver Quest geprüft  
    "pools": \[  
      {  
        "rolls": 1,  
        "items": \[  
          // 30% Chance PRO KILL, das Quest-Item zu erhalten  
          { "item\_id": "janes\_lost\_amulet", "quantity": 1, "chance": 0.3 }   
        \]  
      }  
    \]  
  }  
}

## **B) Loot-Tabellen-Liste (Inhalt für config/loot\_tables.json5)**

### **Loot-Tabellen: Gegner (Tier 1\)**

**lt\_goblin\_base** (wird von base\_goblin genutzt)

* **Pool 1 (Garantiert, Wähle 1):**  
  * {"item\_id": "goblin\_ear", "quantity": 1, "chance": 1.0}  
* **Pool 2 (Materialien, Wähle 1):**  
  * {"item\_id": "scrap\_leather", "quantity": \[1, 3\], "chance": 0.4}  
  * {"item\_id": "linen\_cloth", "quantity": \[1, 2\], "chance": 0.4}  
  * {"item\_id": "broken\_sword\_hilt", "quantity": 1, "chance": 0.1}  
* **Pool 3 (Selten, Wähle 1):**  
  * {"item\_id": "potion\_heal\_small", "quantity": 1, "chance": 0.05}  
  * {"item\_id": "blueprint\_iron\_dagger", "quantity": 1, "chance": 0.01}

**lt\_bandit\_base** (wird von base\_bandit genutzt)

* **Pool 1 (Plunder, Wähle 1):**  
  * {"item\_id": "faded\_scroll", "quantity": 1, "chance": 0.5}  
* **Pool 2 (Materialien, Wähle 1):**  
  * {"item\_id": "potion\_heal\_small", "quantity": 1, "chance": 0.2}  
  * {"item\_id": "linen\_cloth", "quantity": \[1, 3\], "chance": 0.3}  
  * {"item\_id": "scrap\_leather", "quantity": \[1, 3\], "chance": 0.3}  
* **Pool 3 (Selten, Wähle 1):**  
  * {"item\_id": "silver\_ring", "quantity": 1, "chance": 0.05}  
  * {"item\_id": "pattern\_leather\_cap", "quantity": 1, "chance": 0.02}  
  * {"item\_id": "blueprint\_iron\_sword", "quantity": 1, "chance": 0.02}

**lt\_beast\_base** (wird von base\_beast genutzt)

* **Pool 1 (Garantiert, Wähle 1):**  
  * {"item\_id": "scrap\_leather", "quantity": \[1, 4\], "chance": 0.6}  
* **Pool 2 (Selten, Wähle 1):**  
  * {"item\_id": "wolf\_pelt", "quantity": 1, "chance": 0.1}  
  * {"item\_id": "red\_herb", "quantity": \[1, 2\], "chance": 0.15}

**lt\_undead\_base** (wird von base\_undead genutzt)

* **Pool 1 (Garantiert, Wähle 1):**  
  * {"item\_id": "ectoplasm", "quantity": 1, "chance": 0.3}  
* **Pool 2 (Materialien, Wähle 1):**  
  * {"item\_id": "linen\_cloth", "quantity": \[1, 2\], "chance": 0.4}  
  * {"item\_id": "dull\_crystal", "quantity": 1, "chance": 0.1}  
* **Pool 3 (Selten, Wähle 1):**  
  * {"item\_id": "recipe\_mana\_small", "quantity": 1, "chance": 0.02}  
  * {"item\_id": "ring\_of\_mana\_small", "quantity": 1, "chance": 0.01}

### **Loot-Tabellen: Gegner (Tier 2\)**

**lt\_orc\_base** (wird von base\_orc genutzt)

* **Pool 1 (Garantiert, Wähle 1):**  
  * {"item\_id": "orcish\_tusk", "quantity": 1, "chance": 0.5}  
* **Pool 2 (Materialien, Wähle 1):**  
  * {"item\_id": "iron\_ore", "quantity": \[2, 5\], "chance": 0.3}  
  * {"item\_id": "scrap\_leather", "quantity": \[3, 6\], "chance": 0.3}  
* **Pool 3 (Selten, Wähle 1):**  
  * {"item\_id": "armor\_iron\_plate", "quantity": 1, "chance": 0.02} // (Ausrüstung)  
  * {"item\_id": "blueprint\_orcish\_battleaxe", "quantity": 1, "chance": 0.01}

**lt\_harpy\_base** (wird von base\_harpy genutzt)

* **Pool 1 (Garantiert, Wähle 1):**  
  * {"item\_id": "harpy\_feather", "quantity": \[1, 3\], "chance": 0.4}  
* **Pool 2 (Selten, Wähle 1):**  
  * {"item\_id": "chipped\_gemstone", "quantity": 1, "chance": 0.1}  
  * {"item\_id": "recipe\_swiftness\_potion", "quantity": 1, "chance": 0.02}  
  * {"item\_id": "ring\_of\_speed", "quantity": 1, "chance": 0.01}

**lt\_elemental\_base** (wird von base\_elemental genutzt)

* **Pool 1 (Garantiert, Wähle 1):**  
  * {"item\_id": "dull\_crystal", "quantity": \[1, 2\], "chance": 0.3}  
* **Pool 2 (Typ-Spezifisch, Wähle 1):**  
  * // (Logik im LootSystem (S7) prüft Gegner-Subtyp)  
  * {"item\_id": "coal", "quantity": \[2, 4\], "chance": 0.5, "condition\_subtype": "Fire"}  
  * {"item\_id": "obsidian\_shard", "quantity": \[1, 2\], "chance": 0.2, "condition\_subtype": "Ice"}  
  * {"item\_id": "iron\_ore", "quantity": \[3, 5\], "chance": 0.5, "condition\_subtype": "Earth"}

### **Loot-Tabellen: Gegner (Tier 3 / Elite)**

**lt\_construct\_base** (wird von base\_construct genutzt)

* **Pool 1 (Garantiert, Wähle 1):**  
  * {"item\_id": "ancient\_core", "quantity": 1, "chance": 0.1}  
* **Pool 2 (Materialien, Wähle 2):**  
  * {"item\_id": "iron\_ore", "quantity": \[5, 10\], "chance": 0.5}  
  * {"item\_id": "steel\_ingot", "quantity": \[1, 3\], "chance": 0.3}  
  * {"item\_id": "obsidian\_shard", "quantity": \[2, 4\], "chance": 0.2}  
* **Pool 3 (Selten, Wähle 1):**  
  * {"item\_id": "design\_golem\_core\_hammer", "quantity": 1, "chance": 0.02}  
  * {"item\_id": "amulet\_of\_the\_golem", "quantity": 1, "chance": 0.01}

**lt\_spider\_queen** (Nur für spider\_queen)

* **Pool 1 (Garantiert, Wähle 2):**  
  * {"item\_id": "spider\_queen\_venom\_gland", "quantity": 1, "chance": 1.0} // (Quest Item)  
  * {"item\_id": "shadow\_silk", "quantity": \[5, 10\], "chance": 1.0}  
* **Pool 2 (Selten, Wähle 1):**  
  * {"item\_id": "pattern\_spider\_silk\_robe", "quantity": 1, "chance": 0.1}  
  * {"item\_id": "obsidian\_dagger", "quantity": 1, "chance": 0.05}

**lt\_orc\_warchief** (Nur für orc\_warchief)

* **Pool 1 (Garantiert, Wähle 2):**  
  * {"item\_id": "orc\_warchief\_banner", "quantity": 1, "chance": 1.0} // (Quest Item)  
  * {"item\_id": "gold\_goblet", "quantity": \[1, 3\], "chance": 1.0}  
* **Pool 2 (Selten, Wähle 1):**  
  * {"item\_id": "orcish\_battleaxe", "quantity": 1, "chance": 0.2}  
  * {"item\_id": "armor\_steel\_plate", "quantity": 1, "chance": 0.1}  
  * {"item\_id": "blueprint\_steel\_greatsword", "quantity": 1, "chance": 0.05}

**lt\_dread\_knight** (Nur für dread\_knight)

* **Pool 1 (Garantiert, Wähle 1):**  
  * {"item\_id": "ectoplasm", "quantity": \[3, 6\], "chance": 1.0}  
* **Pool 2 (Selten, Wähle 1):**  
  * {"item\_id": "dread\_knight\_sword", "quantity": 1, "chance": 0.05}  
  * {"item\_id": "ring\_of\_the\_vampire", "quantity": 1, "chance": 0.03}

### **Loot-Tabellen: Speziell (Quests)**

**lt\_bandit\_quest\_amulet** (Nur für bandit\_thug)

* **Bedingung:** Wird *zusätzlich* zu lt\_bandit\_base geprüft, wenn Quest q\_lost\_amulet aktiv ist.  
* **Pool 1 (Quest-Drop, Wähle 1):**  
  * {"item\_id": "janes\_lost\_amulet", "quantity": 1, "chance": 0.3}

## **C) Balancing-Checkliste (B2.11)**

(Für den Koordinator beim Review von Balancing-Sprints, z.B. S29)

* \[ \] **XP-Werte konsistent?** (Haben Gegner (GDD-1) XP-Werte, die zum Loot (GDD-6) passen?)  
* \[ \] **KI-Skills vorhanden?** (Haben Gegner, die lt\_orc\_warchief nutzen, auch die Skills (GDD-3), um die Items (GDD-2) zu rechtfertigen?)  
* \[ \] **Quest-Items garantiert?** (Sind Quest-Items wie spider\_queen\_venom\_gland auf 100% Chance gesetzt?)  
* \[ \] **Crafting-Loop geschlossen?** (Droppen die Gegner die *Blueprints* (GDD-2) für die Items, die sie selbst fallen lassen? z.B. Ork droppt blueprint\_orcish\_battleaxe *und* orcish\_battleaxe \- ist das gewollt?)  
* \[ \] **Wirtschaft intakt?** (Ist die Menge an gold\_goblet (Plunder) im Verhältnis zu den Shop-Preisen (GDD-2) ausbalanciert?)