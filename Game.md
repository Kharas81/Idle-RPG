### **1\. Grundprinzipien & Architekturdokument**

Dieser Abschnitt ist das **Gesetzbuch** für unser Projekt. Alles, was wir tun, folgt diesen Regeln.

#### **Technische Grundlagen**

* **Entwicklungsumgebung:** Das Projekt wird in **Google Colab** entwickelt, mit **Google Drive** als Speicher. Verzeichnisse werden mit `!mkdir` angelegt, Dateien mit `%%writefile` erstellt. Das Backend läuft per **Flask/FastAPI**.  
* **API-Zugriff:** Der Webserver wird per **`ngrok`** öffentlich erreichbar gemacht. Die URL wird im **`frontend_tester.html`** für Live-Tests eingetragen  
* **Codequalität:** Wir verwenden konsequent **`ruff`** (Linter) und **`black`** (Formatter), um unseren Code von Anfang an sauber und einheitlich zu halten.

#### **Architektur & Design**

* **Event-System (Entkopplung):** Komponenten reden nicht direkt miteinander. Ein zentraler **`EventManager`** dient als Nachrichten-Hub. Services senden Events (z.B. `battle_service.publish("ON_ENEMY_DEFEATED", data)`), und andere Services abonnieren diese Events, ohne voneinander zu wissen. Das ist der Schlüssel zu einem flexiblen und erweiterbaren System.  
* **Datengetriebenes Design:** Wir schreiben keine Werte wie Lebenspunkte oder Angriffsschaden direkt in den Code. **Alles** kommt aus externen Konfigurationsdateien (z.B. `gegner.json`, `items.json`).

**Datenmodelle & Konventionen:**

* **Enums gegen Magic Strings:** Konsequente Nutzung von Enums (`rpg_project/src/models/enums.py`) für feste Werte.  
* **Pydantic für Datenmodelle:** Strikte Verwendung von Pydantic für alle Datenstrukturen (`rpg_project/src/models/`).

#### 

#### **Visualisierung: Workflow & Architektur**

graph TD  
    subgraph Backend  
        GameLoop\[Game Loop\]  
        Models\[Modelle (Pydantic)\]  
        Services\[Services (Battle, Movement etc.)\]  
        API\[API Endpunkte\]  
        EventManager\[EventManager\]  
    end  
    subgraph Frontend  
        FrontendTester\[frontend\_tester.html\]  
        Viewer\[Web-Viewer\]  
    end  
    Drive\[Google Drive\]  
    Ngrok\[ngrok Tunnel\]

    GameLoop \--\> EventManager  
    Services \-- send \--\> EventManager  
    EventManager \-- notify \--\> Services  
    GameLoop \--\> API  
    API \--\> Ngrok  
    Ngrok \--\> FrontendTester  
    Ngrok \--\> Viewer  
    Models \--\> Drive

#### **Qualitätssicherung & Dokumentation**

* **Test-Strategie (Die 7 Helden):**  
  * **Unit-Test-Held:** Testet einzelne, isolierte Funktionen.  
  * **Integration-Held:** Prüft das Zusammenspiel mehrerer Komponenten.  
  * **Spezialist-Held:** Testet typische Spielabläufe (z.B. einen Kampf).  
  * **Chaos-Affe-Held:** Führt Zufallsaktionen aus, um Fehler zu finden.  
  * **Edge-Case-Held:** Konzentriert sich auf Grenzfälle (z.B. Inventar voll).  
  * **Performance-Held:** Misst Geschwindigkeit und Ressourcen.  
  * **User-Held:** Simuliert einen echten Nutzer.  
* **Dokumentation:**  
  * **Kommentare & Docstrings:** Jede Klasse und Funktion erhält eine klare Beschreibung (Was? Input? Output?).  
  * **Projekt-Doku:** Diese **Roadmap**, ein **README**, ein **Sprint-Log** und das **Workflow-Diagramm** werden aktuell gehalten.

---

### **Roadmap: Idle RPG KI Game v4.0 (Die Umsetzungs-Version)**

**Grundprinzipien:** Die Regeln aus Version 3.1 (Event-System, Datengetriebenes Design, Codequalität, Tests, Doku, Architektur-Diagramm) gelten weiterhin als Fundament für alles Folgende.

---

### **2\. Phasen- & Sprint-Plan**

#### **Phase 0: Vorbereitung**

##### **Sprint S0 – Das Fundament 📝**

* **Letzter Stand:** Die Idee ist im Kopf.  
* **Workflow-Update:** Das Projekt wird initialisiert und strukturiert.  
* **Testrollen:** Keine.  
* **Ziel:** Alles ist perfekt vorbereitet, sodass wir in Sprint 1 direkt mit dem Coden beginnen können.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** Nur Ordner: `mkdir -p rpg_project/src/models rpg_project/src/services rpg_project/src/api tests/unit tests/integration config docs frontend`  
  * **Dokumentation:** `README.md`, `docs/GDD.md`, `docs/ROADMAP.md` (diese Datei).  
* ✅ **Grün, wenn…** die Ordnerstruktur steht und die initialen Doku-Dateien auf GitHub sind.

---

### **Phase 1: Das Kernspiel**

##### **Sprint S1 – Fundament & Daten**

* **Letzter Stand:** Projektstruktur angelegt.  
* **Workflow-Update:** Datenmodelle werden erstellt, die von allen anderen Teilen des Spiels genutzt werden.  
* **Testrollen:** Unit-Test-Held.  
* **Ziel:** Alle Basis-Datenmodelle sind definiert und der Loader kann Konfigurationsdateien fehlerfrei einlesen.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/models/enums.py`, `models/core.py`, `rpg_project/src/services/config_loader.py`.  
  * **Config:** `config/items.json5`, `config/opponents.json5`.  
  * **Tests:** `tests/unit/test_config_loader.py`.  
* ✅ **Grün, wenn…** der Test für den Config-Loader erfolgreich ist.

##### **Sprint S2 – Welt & Ticks**

* **Letzter Stand:** S1 abgeschlossen.  
* **Workflow-Update:** `MovementService` wird in den zentralen `GameLoop` integriert.  
* **Testrollen:** Unit-Test-Held, Integration-Held.  
* **Ziel:** Charaktere können sich auf einer Karte bewegen und stoßen an Wänden.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/models/world.py`, `rpg_project/src/services/movement_service.py`, `rpg_project/src/main.py`.  
  * **Config:** `config/maps/level_1.json5`.  
  * **Tests:** `tests/unit/test_movement_service.py`.  
* ✅ **Grün, wenn…** ein Charakter deterministisch von A nach B bewegt werden kann, ohne durch Wände zu gehen.

##### **Sprint S3 – Battle Engine v1**

* **Letzter Stand:** S2 abgeschlossen.  
* **Workflow-Update:** Die `BattleEngine` wird an den `MovementService` angebunden.  
* **Testrollen:** Unit-Test-Held, Spezialist-Held.  
* **Ziel:** Zwei Entitäten können einen rundenbasierten Kampf beginnen, der schrittweise über eine API gesteuert wird.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/services/battle_engine.py`, `rpg_project/src/api/battle.py`.  
  * **API-Endpunkte:** `POST /battle/start`, `POST /battle/step`, `GET /battle/state`.  
  * **Tests:** `tests/unit/test_battle_engine.py`, `tests/integration/test_battle_api.py`.  
* ✅ **Grün, wenn…** ein API-gesteuerter Testkampf erfolgreich von Anfang bis Ende durchgespielt werden kann.

##### **Sprint S4 – API & Viewer**

* **Letzter Stand:** S3 abgeschlossen.  
* **Workflow-Update:** Allgemeine API-Endpunkte werden erstellt und an den `frontend_tester.html` angebunden.  
* **Testrollen:** User-Held, Integration-Held.  
* **Ziel:** Der Spielzustand kann über die API abgefragt und der "Tick" kann ausgelöst werden.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/api/game_state.py`, `frontend/frontend_tester.html`.  
  * **API-Endpunkte:** `GET /state`, `POST /tick`, `POST /reset`.  
  * **Tests:** `tests/integration/test_game_state_api.py`.  
* ✅ **Grün, wenn…** ein Klick auf einen Button im `frontend_tester.html` (verbunden via `ngrok`\-URL) den Spielzustand im Backend verändert und das Ergebnis anzeigt.

##### **Sprint S5 – Zufall, Lernen & Replays**

* **Letzter Stand:** S4 abgeschlossen.  
* **Workflow-Update:** Ein zentraler `RNGService` steuert allen Zufall im Spiel.  
* **Testrollen:** Chaos-Affe-Held, Edge-Case-Held.  
* **Ziel:** Jede Spielsitzung ist mit demselben Start-Seed zu 100% reproduzierbar.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/services/rng_service.py`, `rpg_project/src/services/replay_service.py`.  
  * **API-Endpunkte:** `POST /replay/save`, `POST /replay/load`.  
  * **Tests:** `tests/unit/test_rng_service.py`, `tests/integration/test_replay_service.py`.  
* ✅ **Grün, wenn…** zwei Spieldurchläufe mit identischem Seed und Aktionen zu einem bit-identischen Spielzustand führen.

##### **Sprint S6 – Sessions & Save/Load**

* **Letzter Stand:** S5 abgeschlossen.  
* **Workflow-Update:** Ein `SessionManager` kümmert sich um das Speichern und Laden.  
* **Testrollen:** Integration-Held, User-Held.  
* **Ziel:** Der Spielfortschritt kann dauerhaft gespeichert und wiederhergestellt werden.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/services/session_manager.py`.  
  * **API-Endpunkte:** `POST /session/new`, `POST /session/save`, `GET /session/load`.  
  * **Tests:** `tests/integration/test_session_manager.py`.  
* ✅ **Grün, wenn…** ein Spielstand erfolgreich auf die Festplatte geschrieben und wiederhergestellt werden kann.

##### **Sprint S7 – RPG-Systeme**

* **Letzter Stand:** S6 abgeschlossen.  
* **Workflow-Update:** Der `Character` wird um RPG-Attribute erweitert; der `RPGService` reagiert auf Events.  
* **Testrollen:** Spezialist-Held, Unit-Test-Held.  
* **Ziel:** Charaktere können aufsteigen, erhalten Beute und verwalten ein Inventar.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/models/character.py` (erweitert), `rpg_project/src/services/rpg_service.py`.  
  * **Config:** `config/game_rules.json5` (XP-Kurve).  
  * **Tests:** `tests/unit/test_rpg_service.py`.  
* ✅ **Grün, wenn…** das `ON_ENEMY_DEFEATED`\-Event korrekt XP und Gold gewährt und ein Level-Up auslöst.

##### **Sprint S8 – Kampf v2**

* **Letzter Stand:** S7 abgeschlossen.  
* **Workflow-Update:** `BattleEngine` wird um Skills, Kosten, Cooldowns und Effekte erweitert.  
* **Testrollen:** Performance-Held, Spezialist-Held.  
* **Ziel:** Der Kampf wird taktischer durch den Einsatz von Fähigkeiten.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/models/effects.py`.  
  * **Config:** `config/skills.json5`.  
  * **Tests:** `tests/unit/test_battle_engine_v2.py`.  
* ✅ **Grün, wenn…** ein Held einen "Feuerball"-Skill nutzen kann, der Schaden verursacht und einen "Brennen"-Effekt hinterlässt.

##### **Sprint S9 – Gegner-KI & Verhalten**

* **Letzter Stand:** S8 abgeschlossen.  
* **Workflow-Update:** Gegner erhalten eine KI, die über simples Angreifen hinausgeht.  
* **Testrollen:** Edge-Case-Held, Chaos-Affe-Held.  
* **Ziel:** Gegner verhalten sich je nach Typ unterschiedlich.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/services/opponent_ai.py`.  
  * **Config:** `config/opponents.json5` (erweitert um `ai_policy`).  
  * **Tests:** `tests/unit/test_opponent_ai.py`.  
* ✅ **Grün, wenn…** ein "feiger Goblin" bei 20% Leben die Flucht ergreift, anstatt weiterzukämpfen.

##### **Sprint S10a – Sammeln & Ressourcen**

* **Letzter Stand:** S9 abgeschlossen.  
* **Workflow-Update:** Spieler können mit der Welt interagieren, um Ressourcen zu sammeln.  
* **Testrollen:** Edge-Case-Held, Integration-Held.  
* **Ziel:** Die Welt wird mit sammelbaren Ressourcen gefüllt.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/models/resource.py`, `rpg_project/src/services/gathering_service.py`.  
  * **API-Endpunkte:** `POST /action/gather`.  
  * **Config:** `config/maps/level_1.json5` (erweitert).  
  * **Tests:** `tests/unit/test_gathering_service.py`.  
* ✅ **Grün, wenn…** ein Spieler zu einer "Eisenerzader" gehen, sie abbauen und "Eisenerz" im Inventar haben kann.

##### **Sprint S10b – Crafting-Logik & Rezepte**

* **Letzter Stand:** S10a abgeschlossen.  
* **Workflow-Update:** Spieler können Ressourcen verwenden, um neue Gegenstände herzustellen.  
* **Testrollen:** Spezialist-Held, Performance-Held.  
* **Ziel:** Ein funktionierendes Crafting-System.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/models/crafting.py`, `rpg_project/src/services/crafting_service.py`.  
  * **API-Endpunkte:** `POST /action/craft`.  
  * **Config:** `config/recipes.json5`.  
  * **Tests:** `tests/unit/test_crafting_service.py`.  
* ✅ **Grün, wenn…** ein Spieler aus 5 Eisenerz erfolgreich ein Eisenschwert herstellen kann.

##### **Sprint S11 – Ausrüstungssystem**

* **Letzter Stand:** S10b abgeschlossen.  
* **Workflow-Update:** Spieler können Gegenstände anlegen, um ihre Werte zu verbessern.  
* **Testrollen:** Unit-Test-Held, Integration-Held.  
* **Ziel:** Ausrüstung hat einen spürbaren Einfluss auf die Charakterstärke.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/services/equipment_service.py`.  
  * **API-Endpunkte:** `POST /character/equip`, `POST /character/unequip`.  
  * **Config:** `config/items.json5` (erweitert um `slot` und `stats`).  
  * **Tests:** `tests/unit/test_equipment_service.py`.  
* ✅ **Grün, wenn…** das Anlegen eines Eisenschwerts (+5 ATK) den Angriffs-Wert des Charakters korrekt um 5 erhöht.

##### **Sprint S12 – Charakterentwicklung & Talentbaum**

* **Letzter Stand:** S11 abgeschlossen.  
* **Workflow-Update:** Ein Talentbaum ermöglicht eine tiefere Spezialisierung.  
* **Testrollen:** User-Held, Edge-Case-Held.  
* **Ziel:** Spieler können permanente Boni und Fähigkeiten freischalten.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/models/talent.py`, `rpg_project/src/services/talent_service.py`.  
  * **API-Endpunkte:** `POST /character/learn_talent`.  
  * **Config:** `config/talents.json5`.  
  * **Tests:** `tests/unit/test_talent_service.py`.  
* ✅ **Grün, wenn…** das Freischalten des Talents "+10% Feuerschaden" den Schaden des Feuerball-Skills korrekt erhöht.

##### **Sprint S13 – Fortschritt, Replay & Statistik**

* **Letzter Stand:** S12 abgeschlossen.  
* **Workflow-Update:** Ein `StatsTracker` sammelt Daten über die Spieler-Session via Event-System.  
* **Testrollen:** Integration-Held, Performance-Held.  
* **Ziel:** Spieler können ihre Erfolge in detaillierten Statistiken einsehen.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/services/stats_tracker.py`.  
  * **API-Endpunkte:** `GET /character/stats`.  
  * **Tests:** `tests/integration/test_stats_tracker.py`.  
* ✅ **Grün, wenn…** nach dem Besiegen von 10 Schleimen der API-Endpunkt `{"slimes_defeated": 10}` zurückgibt.

##### **Sprint S14 – Welt- und Map-Features**

* **Letzter Stand:** S13 abgeschlossen.  
* **Workflow-Update:** Karten werden um interaktive Objekte erweitert.  
* **Testrollen:** Edge-Case-Held, User-Held.  
* **Ziel:** Die Erkundung der Welt wird belohnender.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/models/interactables.py`, `rpg_project/src/services/interaction_service.py`.  
  * **API-Endpunkte:** `POST /action/interact`.  
  * **Config:** `config/maps/level_1.json5` (erweitert).  
  * **Tests:** `tests/unit/test_interaction_service.py`.  
* ✅ **Grün, wenn…** ein Spieler eine Truhe öffnen und den darin enthaltenen Loot erhalten kann.

##### **Sprint S15 – Anzeige (Grafik & Komfort)**

* **Letzter Stand:** S14 abgeschlossen.  
* **Workflow-Update:** Der `frontend_tester.html` wird durch einen ansehnlicheren Web-Viewer ersetzt.  
* **Testrollen:** User-Held.  
* **Ziel:** Eine ansprechende Benutzeroberfläche.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `frontend/viewer.js`, `frontend/viewer.html`.  
  * **Tests:** Manuelle Tests.  
* ✅ **Grün, wenn…** die Spielwelt im Browser grafisch mit Emojis für Spieler, Gegner und Wände dargestellt wird.

##### **Sprint S16 – Qualität & Dev-Tools**

* **Letzter Stand:** S15 abgeschlossen.  
* **Workflow-Update:** Das Projekt wird aufgeräumt und die Testabdeckung erhöht.  
* **Testrollen:** Performance-Held, Edge-Case-Held.  
* **Ziel:** Das Kernspiel ist fertig, stabil und qualitätsgesichert.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `pyproject.toml`, `.github/workflows/ci.yml`.  
  * **Tests:** Code-Coverage über 80% bringen.  
* ✅ **Grün, wenn…** der `ruff` Linter und die gesamte Testsuite bei jedem Push auf GitHub automatisch erfolgreich durchlaufen.

---

### **Phase 2: Erweiterungen & Lebendige Welt**

##### **Sprint S17 – Fraktionen & Rufsystem**

* **Letzter Stand:** S16 abgeschlossen.  
* **Workflow-Update:** Ein `ReputationManager` abonniert Events.  
* **Testrollen:** Integration-Held, Edge-Case-Held.  
* **Ziel:** Aktionen des Spielers haben soziale Konsequenzen.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/models/reputation.py`, `rpg_project/src/services/reputation_manager.py`.  
  * **API-Endpunkte:** `GET /character/reputation`.  
  * **Config:** `config/factions.json5`.  
  * **Tests:** `tests/integration/test_reputation_manager.py`.  
* ✅ **Grün, wenn…** das Töten eines Banditen den Ruf bei der "Stadtwache" erhöht und bei den "Banditen" senkt.

##### **Sprint S18 – NPCs & Dialogsystem**

* **Letzter Stand:** S17 abgeschlossen.  
* **Workflow-Update:** Ein `DialogueManager` steuert Gespräche mit NPCs.  
* **Testrollen:** User-Held, Spezialist-Held.  
* **Ziel:** NPCs bevölkern die Welt und geben Quests.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/models/dialogue.py`, `rpg_project/src/services/dialogue_manager.py`.  
  * **API-Endpunkte:** `POST /npc/talk`, `POST /npc/dialogue_choice`.  
  * **Config:** `config/dialogues/guard.json5`.  
  * **Tests:** `tests/unit/test_dialogue_manager.py`.  
* ✅ **Grün, wenn…** ein Spieler eine Quest von einem NPC über einen Dialog annehmen kann.

##### **Sprint S19 – Begleiter / Pets**

* **Letzter Stand:** S18 abgeschlossen.  
* **Workflow-Update:** Pets werden als Entitäten in `GameLoop` und `BattleEngine` integriert.  
* **Testrollen:** Integration-Held, Chaos-Affe-Held.  
* **Ziel:** Helden erhalten Begleiter mit eigenem Verhalten und Skills.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/models/pet.py`, `rpg_project/src/services/pet_ai.py`.  
  * **API-Endpunkte:** `POST /pet/summon`, `POST /pet/command`.  
  * **Config:** `config/pets.json5`.  
  * **Tests:** `tests/integration/test_pet_combat.py`.  
* ✅ **Grün, wenn…** Pets wie Mini-Helden mitplanbar im Kampf agieren.

##### **Sprint S20 – Offline-Fortschritt**

* **Letzter Stand:** S19 abgeschlossen.  
* **Workflow-Update:** Ein `OfflineProgressCalculator` wird beim Login ausgeführt.  
* **Testrollen:** Performance-Held, Edge-Case-Held.  
* **Ziel:** Ein Spieler wird für seine Abwesenheit belohnt.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/services/offline_progress.py`.  
  * **API-Endpunkte:** `POST /session/login`, `POST /session/logout`.  
  * **Config:** `config/game_rules.json5` (erweitert).  
  * **Tests:** `tests/unit/test_offline_progress.py`.  
* ✅ **Grün, wenn…** ein Spieler nach einer simulierten Pause die korrekte Menge an Ressourcen erhält.

##### **Sprint S21 – Prozedurale Inhalte**

* **Letzter Stand:** S20 abgeschlossen.  
* **Workflow-Update:** Ein `DungeonGenerator` erstellt neue `WorldMap`\-Datenobjekte.  
* **Testrollen:** Chaos-Affe-Held, Performance-Held.  
* **Ziel:** Unendlicher Wiederspielwert durch zufällige Dungeons.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/services/dungeon_generator.py`.  
  * **API-Endpunkte:** `POST /dungeon/enter`.  
  * **Config:** `config/dungeon_rules.json5`.  
  * **Tests:** `tests/unit/test_dungeon_generator.py`.  
* ✅ **Grün, wenn…** mit demselben Seed immer derselbe, spielbare Dungeon generiert wird.

##### **Sprint S22 – Automatisierungs-Management**

* **Letzter Stand:** S21 abgeschlossen.  
* **Workflow-Update:** Ein `AutomationManager` prüft vor der Spieleraktion definierte Regeln.  
* **Testrollen:** User-Held, Edge-Case-Held.  
* **Ziel:** Der Spieler kann die KI seines eigenen Helden konfigurieren.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/models/automation.py`, `rpg_project/src/services/automation_manager.py`.  
  * **API-Endpunkte:** `POST /automation/rules`, `GET /automation/rules`.  
  * **Tests:** `tests/unit/test_automation_manager.py`.  
* ✅ **Grün, wenn…** der Held im Autopilot einen Heiltrank benutzt, sobald seine HP unter einen Schwellenwert fallen.

---

### **Phase 3: Der lernende Held**

##### **Sprint S23 – RL-Grundgerüst**

* **Letzter Stand:** S22 abgeschlossen.  
* **Workflow-Update:** Das Spiel wird in eine `Gymnasium`\-kompatible Umgebung gekapselt.  
* **Testrollen:** Performance-Held, Integration-Held.  
* **Ziel:** Die Grundlage für das Training eines RL-Agenten ist geschaffen.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/rl/environment.py`, `rpg_project/src/rl/spaces.py`.  
  * **Config:** `config/rl_env.json5`.  
  * **Tests:** `tests/integration/test_rl_environment.py`.  
* ✅ **Grün, wenn…** ein Standard-RL-Algorithmus ohne Fehler auf der `RpgEnv` laufen kann.

##### **Sprint S24 – Der lernende Kämpfer**

* **Letzter Stand:** S23 abgeschlossen.  
* **Workflow-Update:** Ein RL-Agent wird an die `BattleEngine` gekoppelt.  
* **Testrollen:** Performance-Held, Spezialist-Held.  
* **Ziel:** Der RL-Agent kann selbstständig Kämpfe bestreiten.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `scripts/train_fighter.py`, `rpg_project/src/rl/agent.py`.  
  * **Tests:** End-to-End-Test: Trainieren, speichern, laden.  
* ✅ **Grün, wenn…** der trainierte Agent einen einfachen "Dummy"-Gegner zuverlässig besiegt.

##### **Sprint S25 – Der effiziente Entdecker & Sammler**

* **Letzter Stand:** S24 abgeschlossen.  
* **Workflow-Update:** Ein neuer RL-Agent für Navigation wird trainiert.  
* **Testrollen:** Performance-Held, Chaos-Affe-Held.  
* **Ziel:** Der RL-Agent kann eine Karte systematisch und optimiert erkunden.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `scripts/train_explorer.py`, `RpgEnv` wird erweitert.  
  * **Config:** `config/rl_env.json5` (erweitert).  
  * **Tests:** Test, der prüft, ob der Agent eine 5x5-Karte schneller erkundet als durch Zufall.  
* ✅ **Grün, wenn…** der Agent eine Karte mit 3 Ressourcenpunkten zuverlässig abfarmt.

##### **Sprint S26 – Der strategische Manager**

* **Letzter Stand:** S25 abgeschlossen.  
* **Workflow-Update:** Ein übergeordneter "Manager-Agent" steuert die spezialisierten Agenten.  
* **Testrollen:** Integration-Held, Spezialist-Held.  
* **Ziel:** Die KI kann das Spiel auf einer strategischen Meta-Ebene spielen.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `scripts/train_manager.py`, `rpg_project/src/rl/manager_agent.py`.  
  * **Tests:** Integrationstest: Ziel "Crafte Item X".  
* ✅ **Grün, wenn…** der Manager-Agent ein einfaches Crafting-Rezept autonom von Anfang bis Ende erfüllen kann.

---

### **Phase 4: Politur & Dynamisches Erlebnis**

##### **Sprint S27 – The Director AI**

* **Letzter Stand:** S26 abgeschlossen.  
* **Workflow-Update:** Eine `DirectorAI` wird in den `GameLoop` integriert.  
* **Testrollen:** Chaos-Affe-Held, User-Held.  
* **Ziel:** Ein unsichtbarer Spielleiter schafft unvorhersehbare Spielerlebnisse.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/services/director_ai.py`.  
  * **Config:** `config/director_events.json5`.  
  * **Tests:** `tests/unit/test_director_ai.py`.  
* ✅ **Grün, wenn…** in einem Testlauf ein dynamisches Event korrekt ausgelöst wird.

##### **Sprint S28 – Sound & Musik**

* **Letzter Stand:** S27 abgeschlossen.  
* **Workflow-Update:** Ein `SoundManager` wird an das Event-System angeschlossen.  
* **Testrollen:** User-Held.  
* **Ziel:** Wichtige Aktionen haben ein befriedigendes Audio-Feedback.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/services/sound_manager.py`.  
  * **Config:** `config/sounds.json5`.  
  * **Tests:** Manuelle Tests.  
* ✅ **Grün, wenn…** bei einem Treffer und einem Level-Up ein Sound zu hören ist.

##### **Sprint S29 – Balancing & Feedback**

* **Letzter Stand:** S28 abgeschlossen.  
* **Workflow-Update:** Keine neuen Systeme, nur Anpassung der Configs.  
* **Testrollen:** Spezialist-Held, User-Held.  
* **Ziel:** Das Spiel fühlt sich fair und motivierend an.  
* **Technische Umsetzung & Meilensteine:**  
  * **Config:** Intensive Anpassung von `items.json5`, `opponents.json5`, etc.  
* ✅ **Grün, wenn…** ein Testspieler sagt: "Das macht Spaß und fühlt sich fair an."

##### **Sprint S30 – Hauptmenü & Packaging**

* **Letzter Stand:** S29 abgeschlossen.  
* **Workflow-Update:** Ein "MainMenu"-State wird vor dem Spielstart eingeführt.  
* **Testrollen:** User-Held.  
* **Ziel:** Das Spiel ist fertig und kann als eine einzige, ausführbare Datei weitergegeben werden.  
* **Technische Umsetzung & Meilensteine:**  
  * **Neue Module:** `rpg_project/src/ui/main_menu.py`, `scripts/build.py` (für `PyInstaller`).  
* ✅ **Grün, wenn…** du einem Freund eine einzelne `.exe`\-Datei (oder Äquivalent) schicken kannst und er das Spiel ohne Installation starten kann.

