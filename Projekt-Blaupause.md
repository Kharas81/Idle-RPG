# **Projekt-Blaupause v5 (Gesetzbuch & Plan)**

Dieser Plan integriert die strategischen Vorschläge (A1-A3, B1-B2) für Robustheit, Skalierbarkeit und Projektmanagement.

## **Inhaltsverzeichnis**

* [Teil 1: Projekt-Blaupause (Das Gesetzbuch)](#bookmark=id.6i3kkgseehkw)  
  * [1.1 Technische Grundlagen (Das "Wo")](#bookmark=id.i5ut472vl99j)  
  * [1.2 Architektur & Design (Das "Wie")](#bookmark=id.1s8rkiw5r4kt)  
  * [1.3 Visualisierung: Architektur-Überblick (farbig)](#bookmark=id.3qaect2f36i6)  
  * [1.4 Qualitätssicherung & Dokumentation (Das "Korrektiv")](#bookmark=id.r1n2cjo4w53q)  
* [Teil 2: Detaillierter Implementierungsplan (v5.0-ECS)](#bookmark=id.6eil70z2kw4n)  
  * [Phase 0: Vertikaler Prototyp (Risiko-Management)](#bookmark=id.vorv7mne9r20)  
  * [Phase 1: Das Kernspiel (ECS-basiert)](#bookmark=id.opaqvp98c8do)  
  * [Phase 2: RPG-Tiefe & KI](#bookmark=id.xawyko3ksrj6)  
  * [Phase 3: Welt-Interaktion (ECS-basiert)](#bookmark=id.alzz5efqsdf1)  
  * [Phase 4: Politur & Abschluss](#bookmark=id.c6vdrtx9een)  
  * [Phase 5: Erweiterungen & Lebendige Welt](#bookmark=id.5blc5teehzv3)  
  * [Phase 6: Der lernende Held (RL)](#bookmark=id.nf5lnwkqjfa)  
  * [Phase 7: Politur & Dynamisches Erlebnis](#bookmark=id.ulyzk69bbawi)  
* [Teil 3: Projekt-Status](#bookmark=id.n0z263klc6su)

## **Teil 1: Projekt-Blaupause (Das Gesetzbuch)**

Dieser Abschnitt ist das **Gesetzbuch** für unser Projekt. Alle Sprints müssen sich an diese Regeln halten.

### **1.1 Technische Grundlagen (Das "Wo")**

1. **Entwicklungs-Philosophie (A1): Lokal Entwickeln, in Colab Trainieren.**  
   * **Begründung:** Stabilität. Die Entwicklung auf dem PC (mit VS Code, lokaler DB) ist robust. Colab/Ngrok/GDrive ist fragil und nur für das finale GPU-Training (S24+) zu nutzen, nicht für die Sprints S0-S22.  
2. **Quellcode-Verwaltung (A3): Git für ALLES.**  
   * **Begründung:** Absolute Sicherheit und Historie. Nicht nur Code, sondern auch .json5-Configs, .md-Dokumente (GDDs, Pläne) und das ENTWICKLERTAGEBUCH.md gehören ins Git.  
3. **Backend:** Das Kern-Backend läuft als Server (z.B. FastAPI), um eine API bereitzustellen.  
4. **API-Zugriff:** Für das Training wird der Server per ngrok öffentlich erreichbar gemacht.  
5. **Codequalität:** Wir verwenden konsequent ruff (Linter/Formatierer), um Code sauber zu halten.

### **1.2 Architektur & Design (Das "Wie")**

1. **Entity-Component-System (ECS):** Das Kernprinzip.  
   * **Entity:** Eine simple ID (z.B. 123).  
   * **Component:** Ein reiner Datencontainer (z.B. PositionComponent(x=10, y=5)).  
   * **System:** Die reine Logik (z.B. MovementSystem), die Komponenten verarbeitet.  
2. **ECS-Performance (A1): Optimierte "Views".**  
   * **Begründung:** Verhindert Performance-Flaschenhälse. Statt dass Systeme 10.000 Entities durchsuchen (O(N)), sollte der EntityManager optimierte Listen (Views) pflegen, auf die Systeme in O(1) zugreifen können (z.B. eine moving\_entities\_list).  
3. **Tick-Modi:** Die GameLoop (S2) kennt zwei Zustände:  
   * TickMode.REALTIME: Der "Zuschauer-Modus". Langsam, löst alle Systeme aus (inkl. Sound S28, Director AI S27).  
   * TickMode.SIMULATION: Der "Trainings-Modus". Blitzschnell, löst *nur* Kern-Logik aus (Movement, Battle, KI) und überspringt "Show"-Systeme.  
4. **Event-System (A1): Typsichere Events.**  
   * **Begründung:** Verhindert schwer zu findende Bugs durch Tippfehler. Statt Strings (event\_manager.publish("ON\_BATTLE")) sollten Python-Klassen (event\_manager.publish(OnBattleFinishedEvent(...))) genutzt werden. Ein Tippfehler führt so zu einem NameError, nicht zu stillem Versagen.  
5. **Datengetriebenes Design (Configs statt Code):** Alle Spielregeln (Stats, Rezepte) liegen in .json5-Dateien im config/-Ordner.  
6. **Datenbank-Speicherung (SQLite):** Spielstände (der ECS-Zustand) werden in einer effizienten sqlite3-Datenbank gespeichert (S6).  
7. **"Wie läuft ein Tick?" (A2):**  
   * Input (API) → Setzt IntentComponent (z.B. MoveIntent)  
   * GameLoop (Tick) → Ruft Systeme (z.B. MovementSystem)  
   * Systeme → Lesen IntentComponent & andere Komponenten (z.B. Position)  
   * Systeme → Verarbeiten Logik, ändern Komponenten (z.B. Position.x \+= 1\)  
   * Systeme → Entfernen IntentComponent, publishen Events (z.B. OnPlayerMovedEvent)  
   * Output (API) → Liest den neuen State (geänderte Position)

### **1.3 Visualisierung: Architektur-Überblick (farbig)**

graph TD  
    subgraph "Frontend (Browser)"  
        Viewer\[Web-Viewer (S15)\]  
    end  
    subgraph "Infrastruktur"  
        Ngrok\[ngrok Tunnel\]  
        Drive\[Google Drive / Lokaler Speicher\]  
    end  
    subgraph "Backend (Lokal / Colab / FastAPI)"  
        API\[API Endpunkte (S4) \- GRÜN\]  
        GameLoop\[Game Loop (S2)\]  
        EventManager\[EventManager (Typsicher)\]  
        WorldState\[WorldState (ECS Manager) (S2)\]  
        WorldState \-- "Hält O(1) Views" \--\> OptimizedViews(Optimized Views / Listen)

        subgraph "Services (Stateless Logik)"  
            ConfigLoader\[ConfigLoader (S1)\]  
            BattleEngine\[BattleEngine (S3)\]  
            AIService\[AI Service (S9, S19)\]  
            KnowledgeService\[KnowledgeService (S26a)\]  
        end  
        subgraph "Systems (Stateful Ticks) \- BLAU"  
            MovementSystem\[MovementSystem (S2)\]  
            BattleSystem\[BattleSystem (S3)\]  
            RPGSystem\[RPGSystem (S7)\]  
            DirectorSystem\[DirectorAI (S27)\]  
            SoundSystem\[SoundSystem (S28)\]  
            QuestSystem\[QuestSystem (S18)\]  
            div(Weitere... S10-S22)  
        end  
    end  
    subgraph "Daten (Persistent)"  
        Database\[SQLite DB (S6)\]  
        Configs\[Config-Dateien (S1)\]  
    end

    %% Verbindungen  
    Viewer \--\> Ngrok \--\> API  
    API \--\> GameLoop  
    API \--\> Services  
    API \--\> WorldState

    GameLoop \-- "tick(mode)" \--\> Systems

    Systems \-- "Liest O(1)" \--\> OptimizedViews  
    Systems \-- "Schreibt O(N)" \--\> WorldState  
    Services \--\> WorldState  
    Systems \-- "Sendet/Empfängt" \--\> EventManager

    Services \--\> ConfigLoader  
    Systems \--\> ConfigLoader  
    ConfigLoader \--\> Configs

    Drive \-- "Hostet" \--\> Database  
    Drive \-- "Hostet" \--\> Configs  
    API \-- "Save/Load" \--\> Database

### **1.4 Qualitätssicherung & Dokumentation (Das "Korrektiv")**

**Test-Strategie (Die 7 Helden):**

| Held | Name | Aufgabe | Aktiv in Sprints (Beispiele) |
| :---- | :---- | :---- | :---- |
| 🛡️ | **Unit-Test-Held** | Testet isolierte Funktionen. | S1, S3, S5, S7, S8, S9, ... |
| 🤝 | **Integration-Held** | Prüft Zusammenspiel (z.B. API \-\> System). | S2, S3, S4, S6, S16 |
| 🎯 | **Spezialist-Held** | Testet typische Spielabläufe (z.B. 1 Kampf). | S3, S7, S8, S10b, S18, S26b |
| 🐒 | **Chaos-Affe-Held** | Bombardiert API mit Zufallsaktionen (S16). | S16 (primär), S5 (Basis) |
| 🧭 | **Edge-Case-Held** | Testet Grenzfälle (Inventar voll, HP=0). | S7, S8, S12, S14 |
| ⚡ | **Performance-Held** | Misst Geschwindigkeit (z.B. simulate\_ticks). | S20, S23 |
| 👤 | **User-Held** | Simuliert echten Nutzer (Frontend). | S4, S15, S29 |

**Dokumentation:**

1. **Meta-Dokumente (A3):**  
   * docs/DAS\_ZIEL.md: Definiert die "Definition of Fun". (Siehe neue Datei)  
   * docs/ENTWICKLERTAGEBUCH.md: Hält Design-Entscheidungen und Fortschritt fest. (Siehe neue Datei)  
2. **Kommentare & Docstrings:** Jede Klasse und wichtige Funktion erhält eine klare Beschreibung.  
3. **Projekt-Doku:** Dieses Dokument und die GDDs werden aktuell gehalten.

## **Teil 2: Detaillierter Implementierungsplan (v5.0-ECS)**

Dies ist der technische Bauplan, neu geordnet nach dem **"Vertikaler Prototyp"-Prinzip (A1)**. Wir validieren zuerst die Kernarchitektur (S0-S23), bevor wir das Spiel mit Inhalten füllen.

### **🔮 Phase 0: Vertikaler Prototyp (Risiko-Management)**

**Ziel:** Beweisen, dass die Kern-Architektur (ECS ↔ RL-Gym) funktioniert.

#### **Sprint S0 – Das Fundament 📝**

* **Ziel:** Eine leere, aber perfekt strukturierte Projektumgebung schaffen.  
* **Meilenstein 1:** Verzeichnisstruktur erstellen  
  * **Task:** \!mkdir (oder lokal) für alle Module.  
  * **Pfade:** rpg\_project/src/models, rpg\_project/src/services, rpg\_project/src/systems, rpg\_project/src/api, rpg\_project/src/rl, tests/unit, tests/integration, config, docs, frontend, scripts  
* **Meilenstein 2:** Dokumentation initialisieren  
  * **Task:** %%writefile (oder lokal) für README.md und die Projektplan-Dateien (dieses Dokument, DAS\_ZIEL.md, ENTWICKLERTAGEBUCH.md).  
* **Meilenstein 3 (A2):** Setup-Skripte erstellen.  
  * **Task:** requirements.txt (mit fastapi, uvicorn, pytest, ruff, python-json5, gymnasium, stable-baselines3) und scripts/setup.sh (Erstellt venv, führt pip install \-r requirements.txt aus).  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Keine (Nur Setup).  
  * **Szenario:** Ein neuer Entwickler klont das Repo und kann scripts/setup.sh ausführen.  
  * ✅ **Grün, wenn…** alle Verzeichnisse und Doku-Dateien im Git sind und pip install funktioniert.  
* **Risiken / Technische Schulden:** Keine.

#### **Sprint S1 – Fundament & Daten (Config)**

* **Ziel:** Externe .json5-Konfigurationsdateien ("Regelbücher") laden und in Pydantic-Modelle gießen.  
* **Workflow-Integration:** ConfigLoaderService wird von allen zukünftigen Services/Systemen genutzt.  
* **Meilenstein 1:** Config-Datenmodelle (models/)  
  * **Task:** Pydantic-Modelle nur für **Konfigurationsdaten**.  
  * **Neue Module:** rpg\_project/src/models/enums.py, rpg\_project/src/models/config\_models.py.  
  * **Modelle:** ItemConfig(BaseModel), OpponentConfig(BaseModel).  
* **Meilenstein 2:** Config-Loader Service (services/)  
  * **Task:** Ein Singleton-Service, der alle .json5-Dateien lädt und validiert.  
  * **Neue Module:** rpg\_project/src/services/config\_loader.py.  
  * **Logik:** load\_configs(), get\_item\_config(item\_id).  
* **Meilenstein 3:** Konfigurationsdateien (config/)  
  * **Neue Dateien:** config/items.json5, config/opponents.json5.  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Unit-Test-Held (tests/unit/test\_config\_loader.py).  
  * **Szenario:** assert loader.get\_item\_config("potion").name \== "Heiltrank".  
  * **Fehlerquelle (A2):** PydanticValidationError (Tippfehler im JSON5) wird korrekt abgefangen.  
  * ✅ **Grün, wenn…** der Test alle JSON5-Dateien erfolgreich als Pydantic-Objekte validiert.  
* **Risiken / Technische Schulden:** Config-Format könnte sich ändern (Handled by B1 \- Mixin-System).

#### **Sprint S2 – ECS, Welt & Ticks (Architektur-Upgrade 1 & 3\)**

* **Hängt ab von:** S1  
* **Ziel:** Implementierung des Entity-Component-Systems (ECS), einer 2D-Karte und des "Tick-Modus"-GameLoops.  
* **Workflow-Integration:** Dies ist der **neue Kern** der Architektur.  
* **Meilenstein 1:** ECS-Kern (models/ecs.py)  
  * **Task:** Definition der ECS-Struktur (Gesetz 1.2.1).  
  * **Logik:**  
    * Entity \= int (eine simple ID).  
    * Component \= class (z.B. PositionComponent(x: int, y: int)).  
    * EntityManager: create\_entity(), add\_component(e\_id, comp), get\_component(e\_id, CompType). (Mit Platzhalter für A1-Views).  
* **Meilenstein 2:** Welt & GameState (services/)  
  * **Task:** WorldState hält die Karte und alle Entities.  
  * **Neue Module:** rpg\_project/src/services/world\_state.py.  
  * **Logik:** class WorldState: Hält entity\_manager: EntityManager und current\_map: MapConfig.  
* **Meilenstein 3:** Game Loop & Tick-Modi (main.py) (Upgrade 3\)  
  * **Task:** Der "Herzschlag", der Tick-Modi unterscheidet (Gesetz 1.2.2).  
  * **Neue Module:** rpg\_project/src/models/enums.py (erweitert um TickMode.REALTIME, TickMode.SIMULATION).  
  * **Logik:**  
    * class GameLoop:  
    * tick(mode: TickMode): Ruft MovementSystem.update(world\_state), BattleSystem.update(world\_state) etc.  
* **Meilenstein 4:** Movement System (systems/movement\_system.py)  
  * **Task:** Logik, um Entitäten zu bewegen (erstes "System").  
  * **Logik:**  
    * class MovementSystem:  
    * update(world\_state):  
      * for e\_id, pos\_comp, move\_intent in world\_state.get\_entities\_with(PositionComponent, MoveIntentComponent): (Nutzt O(N)-Suche, bis A1 implementiert ist).  
      * Prüfe auf Kollision.  
      * Wenn valide, update pos\_comp.x, pos\_comp.y.  
      * Entferne MoveIntentComponent.  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Unit-Test-Held, Integration-Held.  
  * **Szenario:**  
    * Erstelle Entity player mit PositionComponent(1, 1).  
    * Füge MoveIntentComponent(dx=1, dy=0) hinzu.  
    * Rufe game\_loop.tick(TickMode.SIMULATION).  
    * assert player.get\_component(PositionComponent).x \== 2\.  
  * **Fehlerquelle (A2):** Entity hat nicht alle nötigen Komponenten (z.B. Position vergessen).  
  * ✅ **Grün, wenn…** eine Entität (ID) mit Komponenten (Position) durch ein System (MovementSystem) im GameLoop (Tick) korrekt bewegt wird.  
* **Risiken / Technische Schulden:** ECS-Views (A1) sind noch nicht implementiert. Performance-Risiko bei \>1000 Entities.

#### **Sprint S6 – Sessions & Save/Load (Datenbank-Upgrade)**

* **Hängt ab von:** S2  
* **Ziel:** Den **gesamten** aktuellen ECS-Zustand (WorldState) persistent in einer **SQLite-Datenbank** speichern (Gesetz 1.2.5).  
* **Workflow-Integration:** Essentiell für das RL-Training (reset()) und Spieler-Motivation (A3).  
* **Meilenstein 1:** Session Manager (services/session\_manager.py)  
  * **Task:** Logik zum Serialisieren/Deserialisieren des WorldState (S2) in eine .db-Datei.  
  * **Logik:**  
    * DB\_PATH \= 'saves/game.db'  
    * init\_database(): CREATE TABLE IF NOT EXISTS components\_position (...), CREATE TABLE IF NOT EXISTS components\_stats (...) etc. (Eine Tabelle pro Komponententyp).  
    * save\_game(): Holt world\_state (S2). DELETE FROM ... (alle Tabellen leeren). for e\_id, pos in world\_state.get\_entities\_with(PositionComponent): db.execute("INSERT INTO components\_position (e\_id, x, y) VALUES (?, ?, ?)", (e\_id, pos.x, pos.y)). Wiederhole für **jede** Komponente. db.commit().  
    * load\_game(): Liest alle Daten aus der game.db. Rekonstruiert den EntityManager im WorldState (S2).  
* **Meilenstein 2 (A3):** DB-Migration.  
  * **Task:** init\_database() erstellt eine meta-Tabelle (CREATE TABLE meta (key TEXT, value TEXT)).  
  * **Logik:** Beim Init wird INSERT INTO meta (key, value) VALUES ('version', '1') gesetzt. load\_game() prüft die Version.  
* **Meilenstein 3:** API-Endpunkte (api/session.py)  
  * **API:** POST /session/save, GET /session/load, POST /session/new.  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Integration-Held (tests/integration/test\_session\_manager.py).  
  * **Szenario:**  
    * POST /reset (erstellt leere game.db mit version: 1).  
    * POST /tick (Entity 1 bewegt sich zu x=1).  
    * POST /session/save (speichert e\_id=1, x=1 in die DB).  
    * POST /tick (Entity 1 bewegt sich zu x=2).  
    * GET /session/load (lädt x=1 aus der DB).  
    * GET /state: Assert pos.x \== 1\.  
  * ✅ **Grün, wenn…** ein ECS-Spielstand erfolgreich in die sqlite3-Datenbank geschrieben und fehlerfrei wiederhergestellt werden kann.  
* **Risiken / Technische Schulden:** Schema-Änderungen in S7/S8 erfordern manuelles Löschen der DB, bis Migrations-Skripte (Sxx) existieren.

#### **Sprint S23 – RL-Grundgerüst (Gym-Environment)**

* **Hängt ab von:** S2 (Kern-Loop), S1 (Configs), S6 (für reset())  
* **Ziel:** Das gesamte ECS-Backend (S1-S22) in eine gymnasium.Env-kompatible Umgebung zu kapseln. **Dies ist der wichtigste Sprint.**  
* **Workflow-Integration:** Die "RL-KI" (Simulator-Mode). Dies ist der Wrapper für das RL-Training.  
* **Meilenstein 1:** RL Environment (rl/environment.py)  
  * **Task:** Die RpgEnv-Klasse schreiben.  
  * **Logik:**  
    * class RpgEnv(gym.Env):  
    * \_\_init\_\_(self, ...): Initialisiert GameLoop (S2) und alle Services/Systeme.  
    * reset(self, seed=None) \-\> Tuple\[obs, info\]: Ruft SessionManager.new\_game() (S6) und RNGService.set\_seed() (S5, *wird in Phase 1 hinzugefügt*). Gibt self.\_get\_observation() zurück.  
    * step(self, action: int) \-\> Tuple\[obs, reward, terminated, truncated, info\]:  
      * Übersetzt action (z.B. int 5\) in eine API-Aktion (z.B. {"action\_type": "skill", ...}).  
      * world\_state.add\_component(player\_e\_id, ActionRequestComponent(action=...)) (S3).  
      * game\_loop.tick(mode=TickMode.SIMULATION) (Gesetz 1.2.2).  
      * obs \= self.\_get\_observation().  
      * terminated \= self.\_is\_terminated(obs).  
      * reward \= self.\_calculate\_reward(old\_obs, obs).  
      * return obs, reward, terminated, ...  
    * \_get\_observation(self) \-\> dict: Liest direkt aus dem WorldState (S2) (alle relevanten Komponenten des Spielers und der Gegner).  
* **Meilenstein 2:** RL Spaces (rl/spaces.py)  
  * **Task:** observation\_space und action\_space definieren.  
  * **Logik:**  
    * observation\_space: gym.spaces.Dict (ECS-basiert: {"pos": Box, "stats": Box, "inventory": MultiBinary, ...}).  
    * action\_space: gym.spaces.Discrete(N) (Alle Aktionen: Skills, Items, Bewegung).  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Performance-Held (tests/integration/test\_rl\_environment.py).  
  * **Szenario:** pip install gymnasium stable-baselines3, from stable\_baselines3.common.env\_checker import check\_env, env \= RpgEnv(), check\_env(env).  
  * **Fehlerquelle (A2):** observation\_space und \_get\_observation() sind nicht synchron (Form-Fehler).  
  * ✅ **Grün, wenn…** der gymnasium Env-Checker (check\_env) die RpgEnv ohne Fehler validiert.  
* **Risiken / Technische Schulden:** Die Spaces sind noch minimal (nur Position/HP). Belohnung ist rudimentär. **Das Kernrisiko (Architektur-Kompatibilität) ist jedoch validiert.**

### **🧩 Phase 1: Das Kernspiel (ECS-basiert)**

**Ziel:** Aufbau der grundlegenden Spielmechaniken auf dem validierten Prototyp.

#### **Sprint S3 – Battle Engine v1 (ECS-kompatibel)**

* **Hängt ab von:** S2  
* **Ziel:** Eine rundenbasierte 1-gegen-1-Kampf-Engine, die über API gesteuert wird.  
* **Workflow-Integration:** Das MovementSystem (S2) *erstellt* eine BattleSession, wenn Entitäten kollidieren. Das BattleSystem (neu) verarbeitet diese Sessions.  
* **Meilenstein 1:** Kampf-Komponenten (models/ecs.py)  
  * **Task:** Definition von Kampf-Komponenten.  
  * **Komponenten:**  
    * StatsComponent(hp: int, atk: int, def: int)  
    * InBattleComponent(battle\_id: str) (Markiert eine Entity als "gesperrt" für Movement)  
    * ActionRequestComponent(action: dict) (Trägt die API-Aktion von S4)  
* **Meilenstein 2:** Battle Engine & System (services/battle\_engine.py, systems/battle\_system.py)  
  * **Task:** Rundenlogik (Service) getrennt von der Tick-Logik (System).  
  * **Logik:**  
    * BattleEngine (Service): Verwaltet BattleSession-Objekte (hält turn\_order, battle\_state).  
    * BattleSystem (System):  
      * update(world\_state):  
      * for e\_id, action in world\_state.get\_entities\_with(ActionRequestComponent):  
        * Finde battle \= battle\_engine.get\_battle\_for\_entity(e\_id).  
        * battle.process\_step(action) (die Schadenslogik).  
        * Wenn Kampf vorbei: battle\_engine.end\_battle(), sende OnBattleFinishedEvent (A1), entferne InBattleComponent.  
* **Meilenstein 3:** API-Definition (api/battle.py)  
  * **Task:** API-Endpunkte, die **Komponenten** setzen.  
  * **API-Endpunkte:**  
    * POST /battle/start: Ruft battle\_engine.start\_battle() auf.  
    * GET /battle/{battle\_id}/state: Liest direkt aus der BattleEngine.  
    * POST /battle/{battle\_id}/step:  
      * **Aktion:** Setzt die ActionRequestComponent auf die Spieler-Entity. Der BattleSystem-Tick (S2) verarbeitet sie automatisch.  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Spezialist-Held (tests/integration/test\_battle\_api.py).  
  * **Szenario:**  
    * Erstelle 2 Entities mit StatsComponent.  
    * POST /battle/start.  
    * POST /step (setzt ActionRequestComponent).  
    * Rufe game\_loop.tick(TickMode.SIMULATION).  
    * GET /battle/state: Assert HP des Ziels ist gesunken.  
  * ✅ **Grün, wenn…** ein API-gesteuerter Kampf (via ActionRequestComponent) im BattleSystem-Tick korrekt verarbeitet wird.  
* **Risiken / Technische Schulden:** Noch keine KI (S9) oder Skills (S8).

#### **Sprint S4 – API & Viewer**

* **Hängt ab von:** S3  
* **Ziel:** Globale API (für GET /state und POST /tick) und Anbindung an frontend\_tester.html.  
* **Workflow-Integration:** Verbindet das ECS-Backend (S2) mit dem ngrok-Frontend (Gesetz 1.1).  
* **Meilenstein 1:** Globale API-Endpunkte (api/game\_state.py)  
  * **API-Endpunkte:**  
    * GET /state:  
      * **Aktion:** Serialisiert den WorldState (S2) – iteriert über alle Entities und ihre Komponenten.  
      * **Output:** { "map": {...}, "entities": \[{"id": 1, "components": {"pos": {"x":1}, "stats": {"hp":100}}}\] }  
    * POST /tick:  
      * **Aktion:** Ruft game\_loop.tick(mode=TickMode.REALTIME) (S2) genau einmal auf (Gesetz 1.2.2).  
    * POST /reset:  
      * **Aktion:** Setzt WorldState zurück (ruft SessionManager.new\_game()).  
* **Meilenstein 2:** Frontend-Tester (frontend/frontend\_tester.html)  
  * **Task:** Minimale HTML/JS-Datei zum Testen der API.  
  * **Logik:** ngrok-URL-Feld, "Tick"-Button (ruft POST /tick), \<pre\>-Tag für JSON-Output.  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** User-Held (Manuell), Integration-Held.  
  * **Szenario (User-Held):**  
    * Starte Colab-Server und ngrok.  
    * Trage URL in frontend\_tester.html ein.  
    * Klicke "Tick" \-\> JSON im \<pre\>-Tag ändert sich (z.B. pos.x ändert sich).  
  * ✅ **Grün, wenn…** ein Klick auf "Tick" im frontend\_tester.html den GameLoop (im REALTIME-Modus) auslöst und der neue ECS-Zustand angezeigt wird.  
* **Risiken / Technische Schulden:** GET /state serialisiert den *gesamten* WorldState, was bei S20 langsam wird.

#### **Sprint S5 – Zufall, Lernen & Replays**

* **Hängt ab von:** S2  
* **Ziel:** 100% reproduzierbare Spieldurchläufe durch einen zentralen, geseedeten RNGService.  
* **Workflow-Integration:** Essentieller Service, der von BattleSystem (S8), RPGSystem (S7), DungeonGenerator (S21) genutzt wird.  
* **Meilenstein 1:** RNG Service (services/rng\_service.py)  
  * **Task:** Kapselt eine random.Random-Instanz.  
  * **Logik:** set\_seed(seed), get\_int(min, max), get\_float().  
* **Meilenstein 2:** Replay Service & API (services/replay\_service.py)  
  * **Task:** Speichern/Laden von **Aktions-Skripten**.  
  * **API:** POST /replay/save, POST /replay/load.  
* **Meilenstein 3:** API-Endpunkt (api/game\_state.py)  
  * **API:** POST /game/set\_seed (ruft RNGService.set\_seed()).  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Chaos-Affe-Held (tests/integration/test\_replay\_service.py).  
  * **Szenario:**  
    * POST /reset, POST /game/set\_seed (mit seed=123).  
    * Führe Aktionen aus. Speichere finalen GET /state (State A).  
    * POST /reset, POST /game/set\_seed (mit seed=123).  
    * Führe dieselben Aktionen aus. Speichere finalen GET /state (State B).  
    * assert State A \== State B.  
  * ✅ **Grün, wenn…** zwei Spieldurchläufe mit identischem Seed und Aktionen zu einem bit-identischen Spielzustand führen.  
* **Risiken / Technische Schulden:** Jedes System, das random statt RNGService nutzt, bricht die Reproduzierbarkeit.

### **🐲 Phase 2: RPG-Tiefe & KI**

#### **Sprint S7 – RPG-Systeme & Komponenten**

* **Hängt ab von:** S3 (Stats), S6 (DB-Schema)  
* **Ziel:** Charaktere um RPG-Kernsysteme (Level, XP, Gold, Inventar) erweitern (Gesetz 1.2.1).  
* **Workflow-Integration:** Statt CharacterModel zu erweitern, fügen wir neue Komponenten hinzu.  
* **Meilenstein 1:** RPG-Komponenten (models/ecs.py)  
  * **Task:** Neue "Bauteile" für RPG-Daten definieren.  
  * **Komponenten:**  
    * XPComponent(current\_xp: int \= 0, xp\_to\_next: int \= 100\)  
    * LevelComponent(level: int \= 1\)  
    * GoldComponent(amount: int \= 0\)  
    * InventoryComponent(items: List\[ItemConfig\] \= \[\])  
    * StatsComponent (aus S3) wird um max\_hp, mana etc. erweitert.  
* **Meilenstein 2:** RPG System (systems/rpg\_system.py)  
  * **Task:** Logik für Belohnungen und Level-Ups, die auf Events reagiert (Gesetz 1.2.3).  
  * **Logik:**  
    * class RPGSystem:  
    * \_\_init\_\_(self, event\_manager): event\_manager.subscribe(OnBattleFinishedEvent, self.handle\_battle\_rewards). (Typsicher, A1)  
    * handle\_battle\_rewards(event: OnBattleFinishedEvent):  
      * winner\_e\_id \= event.winner\_id.  
      * Lade Komponenten: xp\_comp \= world\_state.get\_component(winner\_e\_id, XPComponent). (Ignoriere, wenn Entity keine XP-Komponente hat).  
      * Füge XP/Gold hinzu.  
      * self.check\_level\_up(winner\_e\_id).  
    * check\_level\_up(e\_id): Prüft XPComponent, erhöht LevelComponent, passt StatsComponent an.  
* **Meilenstein 3:** Config (config/game\_rules.json5)  
  * **Task:** XP-Kurve, Level-Stats definieren (Gesetz 1.2.4).  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Spezialist-Held (tests/unit/test\_rpg\_system.py).  
  * **Szenario:**  
    * Erstelle Entity player mit XPComponent und LevelComponent.  
    * Publishe OnBattleFinishedEvent (simuliert S3).  
    * Assert player.get\_component(XPComponent).current\_xp \== 50\.  
    * Publishe Event erneut.  
    * Assert player.get\_component(LevelComponent).level \== 2\.  
  * **Fehlerquelle (A2):** Event-Tippfehler (Handled by A1 \- Typsichere Events).  
  * ✅ **Grün, wenn…** das OnBattleFinishedEvent korrekt die XPComponent und LevelComponent einer Entity modifiziert.  
* **Risiken / Technische Schulden:** InventoryComponent ist nur eine Liste. Randfälle (Inventar voll) nicht behandelt. **DB-Schema (S6) muss aktualisiert werden.**

#### **Sprint S8 – Kampf v2 (Skills & Effekte)**

* **Hängt ab von:** S7 (RPG-Komponenten), S5 (RNG)  
* **Ziel:** Den S3-Kampf taktischer machen (Skills, Mana, Cooldowns, Status-Effekte).  
* **Workflow-Integration:** BattleSystem (S3) wird erweitert. Nutzt RNGService (S5).  
* **Meilenstein 1:** Kampf v2 Komponenten (models/ecs.py)  
  * **Komponenten:**  
    * SkillsComponent(skills: List\[SkillConfig\])  
    * ActiveEffectsComponent(effects: List\[ActiveEffect\]) (z.B. {"id": "burn", "duration": 3})  
    * CooldownsComponent(cooldowns: Dict\[str, int\])  
    * StatsComponent (S3/S7) hat jetzt mana, max\_mana.  
* **Meilenstein 2:** Config (config/skills.json5)  
  * **Task:** Skills (Feuerball, Heilen) mit Kosten, Schaden, Effekten definieren (Gesetz 1.2.4). Implementiert **B1 (Effekt-Motor)**.  
* **Meilenstein 3:** Battle System v2 (systems/battle\_system.py)  
  * **Task:** BattleEngine.process\_step (S3) überarbeiten.  
  * **Logik:**  
    * **Vor** der Aktion: Verarbeite ActiveEffectsComponent (z.B. BURN-Schaden). Reduziere duration und CooldownsComponent.  
    * ActionRequestComponent (S3) kann jetzt {"action\_type": "skill", ...} sein.  
    * **Validierung:** Prüfe StatsComponent.mana, CooldownsComponent.  
    * **Aktion:** Reduziere Mana, setze Cooldown. Nutze RNGService (S5) für Schaden.  
    * **Effekt:** Füge Effekt zur ActiveEffectsComponent des Ziels hinzu.  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Spezialist-Held (tests/unit/test\_battle\_system\_v2.py).  
  * **Szenario:**  
    * POST /step (Aktion: "skill", ID: "fireball").  
    * game\_loop.tick(...).  
    * GET /battle/state: Assert Target hat ActiveEffectsComponent(effects=\["burn"\]), Actor hat CooldownsComponent(cooldowns={"fireball": 3}).  
  * ✅ **Grün, wenn…** ein Held einen "Feuerball"-Skill nutzen kann, der Schaden verursacht und eine "Brennen"-Komponente hinterlässt.  
* **Risiken / Technische Schulden:** Balancing (S29) ist noch nicht existent. **DB-Schema (S6) muss aktualisiert werden.**

#### **Sprint S9 – Gegner-KI & Verhalten**

* **Hängt ab von:** S8  
* **Ziel:** Gegnern "Gehirne" (Skripte) geben, damit sie Skills (S8) nutzen.  
* **Workflow-Integration:** OpponentAIService wird vom BattleSystem (S8) aufgerufen.  
* **Meilenstein 1:** Config Erweitern (config/opponents.json5)  
  * **Task:** Gegner-Config (S1) um KI-Richtlinie und Skills erweitern (Gesetz 1.2.4). Implementiert **B1 (Mixin-System)**.  
  * **Erweiterung:** archetypes: \["base\_goblin", "role\_magic\_light"\] (siehe GDD\_Gegner\_v2.md). ai\_policy: str (z.B. "Coward", "Healer").  
* **Meilenstein 2:** Opponent AI Service (services/opponent\_ai.py)  
  * **Task:** Der "Gehirn"-Service, der die beste Aktion auswählt.  
  * **Logik:** get\_ai\_action(e\_id, world\_state):  
    * Lade OpponentConfig (S1) und StatsComponent (S3) der Entity.  
    * Policy "Healer": if stats.hp / stats.max\_hp \< 0.5: \-\> return {"action\_type": "skill", "skill\_id": "heal\_light"}.  
    * Default: return {"action\_type": "skill", "skill\_id": "basic\_attack", ...}.  
* **Meilenstein 3:** Battle System Integration  
  * **Task:** BattleSystem (S8) muss KI triggern.  
  * **Logik:** update()-Loop: Wenn current\_turn eine Entity mit AIComponent (neue Komponente\!) ist \-\> action \= ai\_service.get\_ai\_action(...) \-\> battle\_engine.process\_step(action).  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Edge-Case-Held (tests/unit/test\_opponent\_ai.py).  
  * **Szenario:**  
    * Starte Kampf gegen "Heiler-Goblin" (Policy: "Healer").  
    * Reduziere HP des Goblins auf 40%.  
    * Triggere den Zug des Goblins.  
    * Assert battle\_log (S3) zeigt "Goblin nutzt Heilung".  
  * ✅ **Grün, wenn…** ein "Heiler-Goblin" (definiert in Config) bei \<50% Leben die Heilung-Aktion wählt.  
* **Risiken / Technische Schulden:** KI ist reaktiv, nicht proaktiv.

### **🌍 Phase 3: Welt-Interaktion (ECS-basiert)**

#### **Sprint S10a – Sammeln & Ressourcen**

* **Hängt ab von:** S7 (Inventar)  
* **Ziel:** Die Welt mit sammelbaren Ressourcen (Erze, Kräuter) füllen.  
* **Workflow-Integration:** Erweitert die Map-Config (S1) und fügt Items zur InventoryComponent (S7) hinzu.  
* **Meilenstein 1:** Ressourcen-Komponente (models/ecs.py)  
  * **Komponenten:** ResourceNodeComponent(item\_id\_reward: str, quantity: int), InteractableComponent() (Marker-Komponente).  
* **Meilenstein 2:** Map Config Erweitern (config/maps/level\_1.json5)  
  * **Task:** Ressourcen auf der Karte platzieren (werden beim Laden von S2 als Entities erstellt).  
* **Meilenstein 3:** Gathering System (systems/gathering\_system.py)  
  * **Logik:** class GatheringSystem: gather\_resource(e\_id: Entity, node\_e\_id: Entity): Validiert Distanz, prüft ResourceNodeComponent, fügt Item zu InventoryComponent (S7).  
* **Meilenstein 4:** API-Endpunkt (api/action.py)  
  * **API:** POST /action/gather (Input: {"node\_e\_id": 123}).  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Integration-Held (tests/unit/test\_gathering\_system.py).  
  * **Szenario:** Spieler-Entity (ID 1\) bei (5,4). Erz-Entity (ID 123\) bei (5,5). POST /action/gather. GET /state: Assert InventoryComponent von ID 1 enthält "Eisenerz".  
  * ✅ **Grün, wenn…** ein Spieler (über API-Call) eine "Eisenerz"-Entity abbauen und das Item in seiner InventoryComponent haben kann.  
* **Risiken / Technische Schulden:** **DB-Schema (S6) muss aktualisiert werden.**

#### **Sprint S10b – Crafting-Logik & Rezepte**

* **Hängt ab von:** S10a (Ressourcen)  
* **Ziel:** Spielern erlauben, Ressourcen (S10a) zu kombinieren, um neue Items (S1) herzustellen.  
* **Workflow-Integration:** Liest recipes.json5 (S1), prüft InventoryComponent (S7).  
* **Meilenstein 1:** Config (config/recipes.json5)  
  * **Task:** Rezepte definieren (z.B. "Eisenschwert" braucht 5 "Eisenerz").  
  * **Modell:** RecipeConfig(BaseModel) (definiert in S1).  
* **Meilenstein 2:** Crafting Service (services/crafting\_service.py)  
  * **Task:** Die Herstellungslogik (Service, kein System, da es kein tick braucht).  
  * **Logik:** class CraftingService: craft\_item(e\_id: Entity, recipe\_id: str): Lade Rezept (S1) und inv\_comp (S7). Prüfe, ob inv\_comp alle recipe.ingredients hat. Wenn ja: Entferne Items, füge recipe.output\_item\_id hinzu. event\_manager.publish(OnItemCraftedEvent(...)).  
* **Meilenstein 3:** API-Endpunkt (api/action.py)  
  * **API:** POST /action/craft (Input: {"recipe\_id": "iron\_sword"}).  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Spezialist-Held (tests/unit/test\_crafting\_service.py).  
  * **Szenario:** Spieler hat 10 "Eisenerz". POST /action/craft. GET /state: Assert InventoryComponent enthält "Eisenschwert" und nur noch 5 "Eisenerz".  
  * ✅ **Grün, wenn…** ein Spieler (via Spezialist-Held-Test) aus 5 Eisenerz erfolgreich ein Eisenschwert herstellen kann.  
* **Risiken / Technische Schulden:** Keine.

#### **Sprint S11 – Ausrüstungssystem (ECS-basiert)**

* **Hängt ab von:** S7 (Inventar), S8 (Stats)  
* **Ziel:** Spielern erlauben, Items (S1) anzulegen, was ihre StatsComponent (S3) modifiziert.  
* **Meilenstein 1:** Ausrüstungs-Komponente (models/ecs.py)  
  * **Komponente:** EquipmentComponent(slots: Dict\[EquipmentSlot, Optional\[ItemConfig\]\]) (z.B. slots\[EquipmentSlot.WEAPON\] \= ...).  
  * **Config Erweitern (items.json5):** Items (S1) bekommen slot: "Weapon" und stats\_bonus: {"atk": 5}.  
* **Meilenstein 2:** Equipment Service (services/equipment\_service.py)  
  * **Task:** Logik zum An- und Ablegen (Service, kein System).  
  * **Logik:** equip\_item(e\_id: Entity, item\_id: str): Lade inv\_comp (S7) und equip\_comp (S11). Finde Item im Inventar. Setze equip\_comp.slots\[item.slot\] \= item. Entferne Item aus inv\_comp. Rufe rpg\_system.recalculate\_stats(e\_id) (S7) auf.  
* **Meilenstein 3:** RPG System (S7) Erweitern  
  * **Task:** Stats neu berechnen.  
  * **Logik recalculate\_stats(e\_id):** Lade stats\_comp (S3), level\_comp (S7), equip\_comp (S11). Setze Stats auf Basis-Level-Werte. for item in equip\_comp.slots.values(): Addiere item.stats\_bonus.  
* **Meilenstein 4:** API-Endpunkte (api/character.py)  
  * **API:** POST /character/equip, POST /character/unequip.  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Unit-Test-Held (tests/unit/test\_equipment\_service.py).  
  * **Szenario:** GET /state: Assert StatsComponent.atk \== 10\. Spieler hat "Eisenschwert" (+5 ATK) in InventoryComponent. POST /character/equip. GET /state: Assert StatsComponent.atk \== 15\.  
  * ✅ **Grün, wenn…** das Anlegen eines Eisenschwerts die StatsComponent korrekt modifiziert.  
* **Risiken / Technische Schulden:** Stats-Berechnung (Boni) kann komplex werden (additiv vs. multiplikativ). **DB-Schema (S6) muss aktualisiert werden.**

#### **Sprint S12 – Charakterentwicklung & Talentbaum**

* **Hängt ab von:** S11 (Stats-Neuberechnung)  
* **Ziel:** Ein Talentbaum für permanente Boni und Skills.  
* **Meilenstein 1:** Talent-Komponente (models/ecs.py)  
  * **Komponenten:** TalentComponent(learned\_talents: List\[str\] \= \[\]), TalentPointsComponent(points: int \= 0).  
* **Meilenstein 2:** Config (config/talents.json5)  
  * **Task:** Talentbaum definieren (Gesetz 1.2.4).  
  * **Modell:** TalentConfig(BaseModel) (definiert in S1) mit id, cost, bonus: {"fire\_damage\_multiplier": 0.1}.  
* **Meilenstein 3:** Talent Service (services/talent\_service.py)  
  * **Task:** Logik zum Erlernen von Talenten.  
  * **Logik:** learn\_talent(e\_id: Entity, talent\_id: str): Lade talent\_comp, points\_comp und talent\_config. Validierung (Punkte, Voraussetzungen). Wenn ja: points\_comp.points \-= cost, talent\_comp.learned\_talents.append(talent\_id). Rufe rpg\_system.recalculate\_stats(e\_id) (S11) auf.  
* **Meilenstein 4:** API-Endpunkt (api/character.py)  
  * **API:** POST /character/learn\_talent.  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Edge-Case-Held (tests/unit/test\_talent\_service.py).  
  * **Szenario:** Spieler hat 1 Talentpunkt. POST /step (Feuerball), messe Schaden (20). POST /character/learn\_talent (ID: "+10% Feuerschaden"). POST /step (Feuerball), messe Schaden (Assert 22).  
  * ✅ **Grün, wenn…** das Freischalten eines Talents den Schaden des "Feuerball"-Skills korrekt erhöht.  
* **Risiken / Technische Schulden:** **DB-Schema (S6) muss aktualisiert werden.**

#### **Sprint S13 – Fortschritt, Replay & Statistik**

* **Hängt ab von:** S7 (Events)  
* **Ziel:** Einen StatsTrackerService implementieren, der passiv Events lauscht, um Metriken zu sammeln.  
* **Workflow-Integration:** Reiner "Zuhörer" am EventManager (Gesetz 1.2.3).  
* **Meilenstein 1:** Stats-Komponente (models/ecs.py)  
  * **Komponente:** StatsTrackerComponent(enemies\_defeated: int \= 0, damage\_dealt: int \= 0, ...)  
* **Meilenstein 2:** Stats Tracker System (systems/stats\_tracker\_system.py)  
  * **Task:** Der "Strichlisten-Service" als System.  
  * **Logik:**  
    * class StatsTrackerSystem:  
    * \_\_init\_\_(self, event\_manager): event\_manager.subscribe(OnEnemyDefeatedEvent, self.on\_enemy\_defeated).  
    * on\_enemy\_defeated(event: OnEnemyDefeatedEvent):  
      * winner\_e\_id \= event.winner\_id.  
      * stats\_comp \= world\_state.get\_component(winner\_e\_id, StatsTrackerComponent).  
      * if stats\_comp: stats\_comp.enemies\_defeated \+= 1\.  
* **Meilenstein 3:** API-Endpunkt (api/character.py)  
  * **API:** GET /character/stats (Liest die StatsTrackerComponent der Spieler-Entity).  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Integration-Held (tests/integration/test\_stats\_tracker.py).  
  * **Szenario:** GET /character/stats: Assert enemies\_defeated \== 0\. Publishe 10x OnEnemyDefeatedEvent. GET /character/stats: Assert enemies\_defeated \== 10\.  
  * ✅ **Grün, wenn…** das Besiegen von 10 Schleimen die StatsTrackerComponent korrekt auf 10 setzt.  
* **Risiken / Technische Schulden:** **DB-Schema (S6) muss aktualisiert werden.**

#### **Sprint S14 – Welt- und Map-Features**

* **Hängt ab von:** S10a (Basis-Interaktion)  
* **Ziel:** Die Welt interaktiver machen (Kisten, Hebel).  
* **Workflow-Integration:** Ähnlich wie S10a (Sammeln).  
* **Meilenstein 1:** Interaktions-Komponenten (models/ecs.py)  
  * **Komponenten:** InteractableComponent() (Marker), ChestComponent(loot\_table\_id: str, is\_looted: bool \= False).  
* **Meilenstein 2:** Interaction Service (services/interaction\_service.py)  
  * **Task:** Logik für "Benutzen" oder "Öffnen".  
  * **Logik:** class InteractionService: interact\_with\_object(e\_id: Entity, object\_e\_id: Entity): Lade chest\_comp \= world\_state.get\_component(object\_e\_id, ChestComponent). Validierung: Distanz, is\_looted \== False. if chest\_comp: rpg\_system.add\_loot(e\_id, chest\_comp.loot\_table\_id). chest\_comp.is\_looted \= True.  
* **Meilenstein 3:** API-Endpunkt (api/action.py)  
  * **API:** POST /action/interact (Input: {"object\_e\_id": 456}).  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Edge-Case-Held (tests/unit/test\_interaction\_service.py).  
  * **Szenario:** Spieler (ID 1\) interagiert mit Kiste (ID 456). POST /action/interact. GET /state: Assert InventoryComponent (S7) von ID 1 enthält "Heiltrank". Assert ChestComponent (S14) von ID 456 hat is\_looted \= True.  
  * ✅ **Grün, wenn…** ein Spieler eine "Kisten"-Entity öffnen und den Loot in seiner InventoryComponent erhalten kann.  
* **Risiken / Technische Schulden:** **DB-Schema (S6) muss aktualisiert werden.**

### **🖥️ Phase 4: Politur & Abschluss**

#### **Sprint S15 – Anzeige (Grafik & Komfort)**

* **Hängt ab von:** S4 (API)  
* **Ziel:** Den frontend\_tester.html (S4) durch einen ansprechenden Web-Viewer (Emojis, DIVs) ersetzen.  
* **Workflow-Integration:** Reiner Frontend-Sprint, der die GET /state-API (S4) konsumiert.  
* **Meilenstein 1:** Frontend-Struktur (frontend/)  
  * **Neue Module:** frontend/viewer.html, frontend/viewer.js, frontend/style.css.  
* **Meilenstein 2:** JavaScript-Logik (viewer.js)  
  * **Task:** API-Aufrufe und DOM-Manipulation (ECS-kompatibel).  
  * **Logik:**  
    * fetch\_state(): Ruft GET /state.  
    * render(state):  
      * render\_map(state.map).  
      * for entity in state.entities:  
        * if(entity.components.pos): render\_entity(entity, entity.components.pos).  
        * if(entity.id \== player\_id): render\_ui(entity) (zeigt stats, inventory etc.).  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** User-Held (Manuelle Tests).  
  * **Szenario:** Öffne viewer.html im Browser. Die Karte wird mit Emojis/DIVs gerendert. Klicke "Tick" \-\> Das Spieler-Emoji bewegt sich sichtbar.  
  * ✅ **Grün, wenn…** die Spielwelt im Browser grafisch dargestellt wird und sich nach einem API-Aufruf sichtbar aktualisiert.  
* **Risiken / Technische Schulden:** DOM-Manipulation ist langsam. Für \>100 Entities wird canvas benötigt.

#### **Sprint S16 – Qualität, CI & Chaos-Affe**

* **Hängt ab von:** S4 (API), S5 (RNG)  
* **Ziel:** Projekt stabilisieren, Testabdeckung (\>80%) erhöhen und CI-Pipeline (GitHub Actions) einrichten.  
* **Workflow-Integration:** Meta-Sprint zur Sicherung der Code-Qualität (Gesetz 1.1).  
* **Meilenstein 1:** Testabdeckung (Code-Coverage)  
  * **Task:** Nutzung von pytest-cov, um Lücken zu finden und Tests zu schreiben.  
  * **Fokus:** Edge-Case-Held (z.B. Was passiert, wenn S6 load\_game fehlschlägt?).  
* **Meilenstein 2 (A2):** CI-Pipeline (.github/workflows/ci.yml)  
  * **Task:** GitHub Actions Workflow-Datei erstellen.  
  * **Logik:** on: \[push\], Jobs für lint\_and\_format (ruff) und test (pytest \--cov). (Siehe Code-Snippet A2).  
* **Meilenstein 3 (A1):** scripts/chaos\_monkey.py.  
  * **Task:** Ein Skript, das die API (S4) nutzt, um RNGService (S5) zu seeden und 10.000 Zufallsaktionen (API-Calls) gegen das Backend zu feuern.  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Alle Helden (automatisiert).  
  * **Szenario:** git push auf GitHub löst CI aus, ruff und pytest laufen grün.  
  * ✅ **Grün, wenn…** chaos\_monkey.py 10.000 Schritte ohne Server-Crash läuft.  
* **Risiken / Technische Schulden:** Chaos-Affe findet ggf. schwer zu reproduzierende Race-Conditions.

### **🌳 Phase 5: Erweiterungen & Lebendige Welt**

#### **Sprint S17 – Fraktionen & Rufsystem**

* **Hängt ab von:** S7 (Events)  
* **Ziel:** Aktionen des Spielers sollen soziale Konsequenzen haben.  
* **Workflow-Integration:** Nutzt Gesetz 1.2.1 (ECS) und 1.2.3 (Events).  
* **Meilenstein 1:** Ruf-Komponente (models/ecs.py)  
  * **Komponente:** ReputationComponent(reputation: Dict\[str, int\]) (z.B. {"city\_guard": 10, "bandits": \-50}).  
* **Meilenstein 2:** Config (config/factions.json5)  
  * **Task:** Fraktionen definieren. opponents.json5 (S1) wird um faction: "bandits" erweitert.  
* **Meilenstein 3:** Reputation System (systems/reputation\_system.py)  
  * **Task:** Logik zur Anpassung des Rufs (reagiert auf Events).  
  * **Logik:** class ReputationSystem: \_\_init\_\_(...): event\_manager.subscribe(OnEnemyDefeatedEvent, self.handle\_kill). handle\_kill(event): Lade loser\_config (S1) und rep\_comp (S17). if rep\_comp and loser\_config.faction \== "bandits": rep\_comp.reputation\["bandits"\] \-= 5\.  
* **Meilenstein 4:** API-Endpunkt (api/character.py)  
  * **API:** GET /character/reputation (Liest ReputationComponent der Spieler-Entity).  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Integration-Held.  
  * **Szenario:** GET /character/reputation: Assert {"bandits": 0}. Publishe OnEnemyDefeatedEvent für einen "Banditen". GET /character/reputation: Assert {"bandits": \-5}.  
  * ✅ **Grün, wenn…** das Töten eines Banditen die ReputationComponent des Spielers korrekt modifiziert.  
* **Risiken / Technische Schulden:** **DB-Schema (S6) muss aktualisiert werden.**

#### **Sprint S18 – NPCs, Dialog- & Questsystem**

* **Hängt ab von:** S17 (Ruf), S14 (Interaktion)  
* **Ziel:** NPCs in der Welt platzieren, die Dialoge führen und Quests vergeben können. (Implementiert **B1: Mark & Jane**).  
* **Workflow-Integration:** InteractionService (S14) wird erweitert. Führt QuestComponent ein.  
* **Meilenstein 1:** Quest- & Dialog-Komponenten (models/ecs.py)  
  * **Komponenten:** DialogueComponent(dialogue\_id: str) (an NPC), QuestComponent(active\_quests: List\[QuestInstance\]) (an Spieler), QuestInstance(quest\_id: str, status: Enum, progress: int).  
* **Meilenstein 2:** Configs (config/dialogues/, config/quests.json5)  
  * **Task:** Dialogbäume und Quests (Ziele: "töte 5 goblin", "sammle 10 erz") schreiben.  
  * **QuestConfig (S1):** id, title, goal: {"type": "kill", "target\_id": "goblin", "count": 5}.  
* **Meilenstein 3:** Dialogue Service & Quest System  
  * **Task:** DialogueService (steuert Gesprächsfluss). QuestSystem (System, prüft Quest-Fortschritt).  
  * **Logik (QuestSystem):** update(world\_state): Prüft active\_quests. \_\_init\_\_(...): event\_manager.subscribe(OnEnemyDefeatedEvent, self.on\_kill). on\_kill(event): Iteriere active\_quests, if quest.goal.target\_id \== event.loser\_id: quest.progress \+= 1\. if quest.progress \>= quest.goal.count: quest.status \= COMPLETED.  
* **Meilenstein 4:** API-Endpunkte (api/npc.py)  
  * **API:** POST /npc/talk, POST /npc/dialogue\_choice.  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Spezialist-Held.  
  * **Szenario:** Spieler nimmt "Töte 5 Goblins"-Quest an. GET /state: Assert QuestComponent hat Quest ACTIVE. Publishe 5x OnEnemyDefeatedEvent. game\_loop.tick(...). GET /state: Assert Quest-Status ist COMPLETED.  
  * ✅ **Grün, wenn…** ein Spieler eine Quest annehmen und durch Töten von Gegnern automatisch abschließen kann.  
* **Risiken / Technische Schulden:** Dialog-JSONs sind mühsam zu schreiben (Handled by B1 \- dialogue\_compiler.py). **DB-Schema (S6) muss aktualisiert werden.**

#### **Sprint S19 – Begleiter / Pets**

* **Hängt ab von:** S18 (NPCs), S9 (KI)  
* **Ziel:** Dem Helden "Pet"-Begleiter an die Seite stellen (eigene Entity, eigene KI).  
* **Workflow-Integration:** Ein Pet ist nur eine Entity (S2) mit StatsComponent (S3), AIComponent (S9) und einer neuen PetComponent.  
* **Meilenstein 1:** Pet-Komponenten (models/ecs.py)  
  * **Komponenten:** PetComponent(owner\_e\_id: Entity, ai\_policy: str) (an Pet), ActivePetComponent(pet\_e\_id: Entity) (an Spieler).  
* **Meilenstein 2:** Config (config/pets.json5)  
  * **Task:** Pets (Wolf, Fee) mit Stats, Skills (S8) und KI-Policies (S9) definieren.  
* **Meilenstein 3:** Pet AI (Erweiterung S9)  
  * **Task:** OpponentAIService (S9) wird zum AIService.  
  * **Logik:** get\_ai\_action kann jetzt "Pet"-Policies verarbeiten (z.B. "folge Besitzer", "greife Ziel des Besitzers an").  
* **Meilenstein 4:** Service-Integration  
  * **Logik:** MovementSystem (S2) muss PetComponent lesen und MoveIntentComponent setzen. BattleSystem (S3) muss ActivePetComponent prüfen und Pet zum Kampf hinzufügen.  
* **Meilenstein 5:** API-Endpunkte (api/pet.py)  
  * **API:** POST /pet/summon, POST /pet/command.  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Integration-Held.  
  * **Szenario:** POST /pet/summon. GET /state: Assert ActivePetComponent beim Spieler. POST /tick: Assert PositionComponent des Wolfs nähert sich Spieler an. Starte Kampf. GET /battle/state: Assert Wolf ist in turn\_order.  
  * ✅ **Grün, wenn…** Pets dem Spieler folgen und im Kampf automatisch mitkämpfen.  
* **Risiken / Technische Schulden:** **DB-Schema (S6) muss aktualisiert werden.**

### **🤖 Phase 6: Der lernende Held (RL)**

#### **Sprint S20 – Simulations-Modus (Vorspulen)**

* **Hängt ab von:** S2 (Tick-Modi)  
* **Ziel:** (Upgrade 3\) Dem Spieler/Beobachter erlauben, das Spiel "vorspulen" zu lassen, indem X Ticks auf einmal simuliert werden.  
* **Workflow-Integration:** Dies ist eine Meta-Funktion, die den GameLoop (S2) im SIMULATION-Modus aufruft (Gesetz 1.2.2).  
* **Meilenstein 1:** Simulation Service (services/simulation\_service.py)  
  * **Task:** Führt den GameLoop schnell und **ohne** "Show"-Systeme aus.  
  * **Logik:** class SimulationService: simulate\_ticks(num\_ticks: int) \-\> dict: for i in range(num\_ticks): game\_loop.tick(mode=TickMode.SIMULATION). (Systeme S27 DirectorAI und S28 SoundManager werden intern übersprungen).  
* **Meilenstein 2:** API-Endpunkte (api/game\_state.py)  
  * **API:** POST /simulate\_ticks (Input: {"num\_ticks": 1000}).  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Performance-Held.  
  * **Szenario:** POST /simulate\_ticks (Input: {"num\_ticks": 1000}). Assert Antwortzeit ist extrem schnell (z.B. \< 1 Sekunde). GET /state: Assert Spielzustand hat sich 1000 Ticks weiterentwickelt.  
  * ✅ **Grün, wenn…** 1000 Ticks im SIMULATION-Modus signifikant schneller verarbeitet werden als 1000 Ticks im REALTIME-Modus.  
* **Risiken / Technische Schulden:** Keine.

#### **Sprint S21 – Prozedurale Inhalte**

* **Hängt ab von:** S5 (RNG), S14 (Kisten)  
* **Ziel:** Unendlichen Wiederspielwert durch zufällige Dungeons.  
* **Workflow-Integration:** DungeonGenerator *erzeugt* Entities (S2) und MapConfig-Objekte (S1). Nutzt RNGService (S5).  
* **Meilenstein 1:** Dungeon Generator (services/dungeon\_generator.py)  
  * **Task:** Logik zur Erstellung einer zufälligen, aber spielbaren Karte.  
  * **Logik:** generate\_dungeon(seed: int, rules: dict) \-\> (MapConfig, List\[Entity\]): Nutzt RNGService (S5). Generiert Wände, platziert Gegner (Entities mit StatsComponent, AIComponent), Kisten (Entities mit ChestComponent).  
* **Meilenstein 2:** Config (config/dungeon\_rules.json5)  
  * **Task:** Regeln für den Generator (Größe, Dichte).  
* **Meilenstein 3:** API-Endpunkt (api/dungeon.py)  
  * **API:** POST /dungeon/enter.  
  * **Aktion:** Ruft generate\_dungeon() auf, world\_state.load\_map(...), world\_state.add\_entities(...).  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Chaos-Affe-Held.  
  * **Szenario:** map\_A, \_ \= generator.generate\_dungeon(seed=123). map\_B, \_ \= generator.generate\_dungeon(seed=123). assert map\_A.wall\_tiles \== map\_B.wall\_tiles.  
  * ✅ **Grün, wenn…** mit demselben Seed immer derselbe, spielbare Dungeon generiert wird.  
* **Risiken / Technische Schulden:** Pfadfindung im Dungeon kann schwierig sein.

#### **Sprint S22 – Automatisierungs-Management (Spieler-KI)**

* **Hängt ab von:** S8 (Skills), S10a (Items)  
* **Ziel:** Dem Spieler (Beobachter) erlauben, eine "Skript-KI" (Wenn-Dann-Regeln) für seinen Helden zu konfigurieren.  
* **Workflow-Integration:** Die "Skript-KI" (Player-Mode).  
* **Meilenstein 1:** Automatisierungs-Komponente (models/ecs.py)  
  * **Komponente:** AutomationComponent(rules: List\[AutomationRule\]).  
  * **Modell:** AutomationRule(BaseModel): condition\_type: Enum (z.B. HP\_BELOW), condition\_value: float, action\_type: Enum, action\_value: str.  
* **Meilenstein 2:** Automation System (systems/automation\_system.py)  
  * **Task:** Prüft und führt Regeln aus. Läuft **vor** dem BattleSystem (S3) und MovementSystem (S2).  
  * **Logik:** update(world\_state): for e\_id, auto\_comp, stats\_comp in world\_state.get\_entities\_with(...): if (check\_condition(rule, stats\_comp)): world\_state.add\_component(e\_id, ActionRequestComponent(action=rule.action)) (S3).  
* **Meilenstein 3:** API-Endpunkte (api/automation.py)  
  * **API:** POST /automation/rules (setzt AutomationComponent), GET /automation/rules.  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** User-Held (tests/unit/test\_automation\_system.py).  
  * **Szenario:** Setze Regel: "Wenn HP \< 30%, nutze Heiltrank". Spieler-HP sinkt auf 25%. game\_loop.tick(...). AutomationSystem läuft, setzt ActionRequestComponent(action="use\_potion"). BattleSystem läuft, führt sie aus. GET /state: Assert Spieler-HP ist geheilt.  
  * ✅ **Grün, wenn…** der Held im Autopilot einen Heiltrank benutzt, sobald seine HP unter einen Schwellenwert fallen.  
* **Risiken / Technische Schulden:** **DB-Schema (S6) muss aktualisiert werden.**

#### **Sprint S24 – Der lernende Kämpfer**

* **Hängt ab von:** S23 (Gym-Env), S8 (Kampf v2)  
* **Ziel:** Einen RL-Agenten (PPO, DQN) darauf zu trainieren, Kämpfe (S8) zu gewinnen.  
* **Workflow-Integration:** Nutzt die RpgEnv (S23) im SIMULATION-Modus.  
* **Meilenstein 1:** Trainings-Skript (scripts/train\_fighter.py)  
  * **Task:** Ein Skript, das stable-baselines3 nutzt, um einen Agenten zu trainieren.  
  * **Logik:** env \= RpgEnv(mode="combat\_only") (Eine Env-Variante, die sofort einen Kampf startet). model \= PPO("MlpPolicy", env, verbose=1). model.learn(total\_timesteps=1\_000\_000). model.save("agents/fighter\_agent\_v1").  
* **Meilenstein 2:** Agenten-Integration (rl/agent.py)  
  * **Task:** Eine Klasse, die den trainierten Agenten lädt und nutzt.  
  * **Logik:** class RLAgent: load\_model(path), get\_action(observation).  
* **Meilenstein 3:** Game Loop Integration (S2)  
  * **Task:** GameLoop kann RL-Agenten anstelle von Spieler-Input verwenden.  
  * **Logik:** if game\_mode \== "RL\_AGENT": action \= rl\_agent.get\_action(obs); env.step(action).  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Spezialist-Held.  
  * **Szenario:** Trainiere Agenten für 1M Schritte gegen einen "Dummy"-Gegner. Lade den trainierten Agenten. Führe 100 Test-Kämpfe aus. Assert win\_rate \> 0.95.  
  * ✅ **Grün, wenn…** der trainierte Agent einen einfachen "Dummy"-Gegner zuverlässig besiegt.  
* **Risiken / Technische Schulden:** Belohnungs-Design (Reward Shaping) ist komplex.

#### **Sprint S25 – Der effiziente Entdecker & Sammler**

* **Hängt ab von:** S23 (Gym-Env), S10a (Sammeln)  
* **Ziel:** Einen zweiten RL-Agenten trainieren (Navigation S2, Sammeln S10a).  
* **Workflow-Integration:** Erweitert die RpgEnv (S23) für Erkundung.  
* **Meilenstein 1:** RpgEnv Erweiterung (rl/environment.py)  
  * **Task:** observation\_space und reward für Erkundung anpassen.  
  * **Logik:** reward: \+100 für das Sammeln einer Ressource (S10a), \-1 für jeden Schritt.  
* **Meilenstein 2:** Trainings-Skript (scripts/train\_explorer.py)  
  * **Task:** Trainiert den neuen Agenten.  
  * **Logik:** env \= RpgEnv(mode="exploration\_only"), model.learn(...), model.save("agents/explorer\_agent\_v1").  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Performance-Held.  
  * **Szenario:** Erstelle Test-Map mit 3 Ressourcen. Lasse explorer\_agent laufen. Assert Agent sammelt 3/3 Ressourcen zuverlässig.  
  * ✅ **Grün, wenn…** der Agent eine Karte mit 3 Ressourcenpunkten zuverlässig abfarmt.  
* **Risiken / Technische Schulden:** Agent könnte lokale Optima finden (z.B. im Kreis laufen).

#### **Sprint S26a – Knowledge & Goal Service (Architektur-Upgrade 2\)**

* **Hängt ab von:** S1 (Configs), S10b (Rezepte)  
* **Ziel:** Eine Wissensdatenbank und ein Ziel-System schaffen, damit der S26b-Agent **weiß**, was er tun soll.  
* **Workflow-Integration:** (Upgrade 2\) Der "Blinde Manager" bekommt sein "Gehirn".  
* **Meilenstein 1:** Knowledge Service (services/knowledge\_service.py)  
  * **Task:** Ein Service, der alle Configs (S1) parst und Abfragen wie "Was brauche ich für X?" beantwortet.  
  * **Logik:** class KnowledgeService: \_\_init\_\_(self, config\_loader): Parst recipes.json5 (S10b), items.json5 (S1) etc. in Graphen. get\_recipe(item\_id: str) \-\> RecipeConfig. get\_item\_source(item\_id: str) \-\> str (z.B. "Erz" \-\> "ResourceNode", "Schwert" \-\> "Crafting").  
* **Meilenstein 2:** Goal-Integration (Erweiterung S18)  
  * **Task:** QuestService (S18) wird zum "Goal-Setter".  
  * **Logik:** Die QuestComponent (S18) der Spieler-Entity ist das **aktive Ziel** für den RL-Agenten.  
  * RpgEnv (S23): observation\_space wird um active\_goal: spaces.Dict(...) erweitert.  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Unit-Test-Held.  
  * **Szenario:** knowledge \= KnowledgeService(config\_loader). recipe \= knowledge.get\_recipe("iron\_sword"). assert recipe.ingredients\["iron\_ore"\] \== 5\.  
  * ✅ **Grün, wenn…** der KnowledgeService erfolgreich alle Config-Abhängigkeiten (Crafting, Sammeln) bereitstellen kann.  
* **Risiken / Technische Schulden:** Wissens-Graph kann komplex werden.

#### **Sprint S26b – Der strategische Manager (H-RL)**

* **Hängt ab von:** S26a (Wissen), S24 (Kämpfer), S25 (Entdecker)  
* **Ziel:** Ein übergeordneter "Manager-Agent" (Hierarchisches RL), der die Sub-Agenten (S24, S25) nutzt, um Quests (S18) zu erfüllen.  
* **Workflow-Integration:** Der "Manager" (Gehirn) nutzt die "Arbeiter" (S24, S25) und das "Wissen" (S26a), um "Ziele" (S18) zu erreichen.  
* **Meilenstein 1:** Manager-Agent (rl/manager\_agent.py)  
  * **Task:** Der Manager-Agent (PPO).  
  * **Logik:**  
    * action\_space (Manager): Discrete(4) (z.B. 0: "Rufe Explorer-Agent", 1: "Rufe Fighter-Agent", 2: "Rufe Crafting-Service", 3: "Rufe Dialogue-Service").  
    * observation\_space (Manager): High-Level (Inventar, QuestComponent, KnowledgeService-Daten).  
* **Meilenstein 2:** Trainings-Skript (scripts/train\_manager.py)  
  * **Task:** Trainiert den Manager.  
  * **Logik:** env \= RpgEnv(mode="full\_game"). env.load\_sub\_agents(fighter\_agent, explorer\_agent). manager\_model \= PPO(...). manager\_model.learn(...) (Der step-Loop ist jetzt hierarchisch).  
* **Meilenstein 3:** RpgEnv Erweiterung (rl/environment.py)  
  * **Task:** Belohnung (reward) für Quest-Abschluss.  
  * **Logik:** reward: \+1000 wenn quest.status \== COMPLETED (S18).  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Spezialist-Held.  
  * **Szenario:** Setze Ziel: Quest "Crafte Eisenschwert" (S18). Starte manager\_agent. Agent muss (basierend auf S26a-Wissen): a. Explorer-Agent (S25) aufrufen, bis 5 Erz in InventoryComponent (S7) sind. b. Crafting-Service (S10b) aufrufen. c. (Quest wird in S18 automatisch abgeschlossen, Agent erhält \+1000 Belohnung).  
  * ✅ **Grün, wenn…** der Manager-Agent autonom eine "Crafte Item"-Quest von Anfang bis Ende erfüllen kann.  
* **Risiken / Technische Schulden:** Extrem komplexes Trainings-Setup.

### **🌳 Phase 7: Politur & Dynamisches Erlebnis**

#### **Sprint S27 – The Director AI**

* **Hängt ab von:** S13 (Statistiken)  
* **Ziel:** Ein "unsichtbarer Spielleiter", der das Spiel dynamisch anpasst (z.B. Gegner spawnen).  
* **Workflow-Integration:** (Upgrade 3\) Dieses System läuft **nur** im REALTIME Tick-Modus (Gesetz 1.2.2).  
* **Meilenstein 1:** Director AI System (systems/director\_ai\_system.py)  
  * **Task:** Logik für dynamische Events.  
  * **Logik:** class DirectorAISystem: update(world\_state, mode: TickMode): if mode \!= TickMode.REALTIME: return. Lade StatsTrackerComponent (S13) (z.B. time\_since\_last\_combat). if stats.time\_since\_last\_combat \> 120: self.spawn\_enemy\_horde(world\_state) (Erstellt 5 Goblin-Entities via S2).  
* **Meilenstein 2:** Config (config/director\_events.json5)  
  * **Task:** Regeln für den Director (Gesetz 1.2.4).  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Chaos-Affe-Held.  
  * **Szenario:** POST /simulate\_ticks(1000) (S20, SIMULATION-Modus). GET /state: Assert keine neuen Gegner (Director hat geschlafen). POST /tick (S4, REALTIME-Modus) 120 Mal. GET /state: Assert 5 neue Goblin-Entities sind gespawnt.  
  * ✅ **Grün, wenn…** ein dynamisches Event **nur** im REALTIME-Modus korrekt ausgelöst wird.  
* **Risiken / Technische Schulden:** Kann das Balancing (S29) stören.

#### **Sprint S28 – Sound & Musik**

* **Hängt ab von:** S15 (Frontend), S7 (Events)  
* **Ziel:** Audio-Feedback für Aktionen im Frontend (S15).  
* **Workflow-Integration:** (Upgrade 3\) SoundSystem sammelt Events und läuft **nur** im REALTIME-Modus (Gesetz 1.2.2).  
* **Meilenstein 1:** Sound System (systems/sound\_system.py)  
  * **Task:** Sammelt Events und leitet sie an den WorldState weiter.  
  * **Logik:** class SoundSystem: \_\_init\_\_(...): event\_manager.subscribe(OnDamageDealtEvent, self.on\_hit). update(world\_state, mode: TickMode): if mode \!= TickMode.REALTIME: self.event\_queue.clear(); return. on\_hit(...): self.event\_queue.append("play:sword\_hit").  
* **Meilenstein 2:** API & Frontend  
  * **Task:** Frontend muss Sounds abspielen.  
  * **API:** GET /state (S4) enthält sound\_events\_this\_tick: List\[str\] (nur gefüllt im REALTIME-Modus).  
  * **Frontend (viewer.js S15):** Spielt Sounds ab, die in der API-Antwort kommen.  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** User-Held (Manuell).  
  * **Szenario:** POST /simulate\_ticks(1000) (schnell, kein Sound). POST /tick (löst Kampf-Event aus). Ein "Schwert-Treffer"-Geräusch ist im Browser zu hören.  
  * ✅ **Grün, wenn…** bei einem Treffer (im REALTIME-Modus) ein Sound zu hören ist.  
* **Risiken / Technische Schulden:** Web-Audio kann Latenz haben.

#### **Sprint S29 – Balancing & Feedback**

* **Hängt ab von:** S1-S28  
* **Ziel:** Das Spiel "spaßig" machen. Anpassung aller Config-Dateien.  
* **Workflow-Integration:** Reiner "Config"-Sprint (Gesetz 1.2.4).  
* **Anmerkung (B1):** Balancing ist ein Prozess, kein Sprint. Dieser Sprint ist der *initiale* Durchlauf. Balancing muss iterativ in S7, S8, S11 etc. erfolgen.  
* **Meilenstein 1:** Balancing-Durchlauf  
  * **Task:** Anpassung aller "Regelbücher" (opponents.json5, game\_rules.json5, recipes.json5, talents.json5).  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** Spezialist-Held, User-Held (Manuelle Spieldurchläufe).  
  * ✅ **Grün, wenn…** ein Testspieler sagt: "Das macht Spaß und fühlt sich fair an."  
* **Risiken / Technische Schulden:** Starke technische Schulden, wenn das Balancing zu stark von den Configs abweicht und Code-Änderungen erfordert.

#### **Sprint S30 – Hauptmenü & Packaging**

* **Hängt ab von:** S29 (Balancing), S15 (Frontend)  
* **Ziel:** Das Spiel fertigstellen (Hauptmenü, optionales PyInstaller-Paket).  
* **Workflow-Integration:** Neuer "State" **vor** dem WorldState (S2).  
* **Meilenstein 1:** Main-Menu-State (ui/main\_menu.py)  
  * **Task:** Logik für "MAIN\_MENU"-Status.  
  * **Logik:** GET /state gibt {"game\_status": "MAIN\_MENU"} zurück.  
  * **Frontend (S15):** Zeigt "Neues Spiel", "Spiel Laden" (S6) Buttons.  
  * **API:** POST /session/new (S6) setzt game\_status auf RUNNING.  
* **Meilenstein 2:** Packaging (Optional)  
  * **Task:** Nutzung von PyInstaller (oder Ähnlichem), um Backend \+ Frontend in eine .exe zu bündeln.  
  * **Neue Module:** scripts/build.py.  
* **Tests & Definition of Done (DoD):**  
  * **Testrollen:** User-Held (Manuell).  
  * **Szenario:** Starte Spiel (Colab oder .exe). Frontend (S15) zeigt Hauptmenü. Klicke "Neues Spiel". Das Spiel (S15-Viewer) startet.  
  * ✅ **Grün, wenn…** du einem Freund eine einzelne .exe-Datei (oder Äquivalent) schicken kannst und er das Spiel ohne Installation starten kann.  
* **Risiken / Technische Schulden:** Packaging von Python-Apps ist notorisch schwierig.

## **Teil 3: Projekt-Status**

(Wird am Ende der Doku gepflegt)

| Phase | Status | Sprint | Status | Anmerkung |
| :---- | :---- | :---- | :---- | :---- |
| 🔮 **P0: Prototyp** | 🔧 In Arbeit | S0 \- Fundament | ✅ |  |
|  |  | S1 \- Configs | ✅ |  |
|  |  | S2 \- ECS-Kern | ✅ |  |
|  |  | S6 \- DB-Speichern | 🔧 | Migration v1 ok |
|  |  | S23 \- Gym-Env | ⚠️ | check\_env ok, aber Spaces rudimentär |
| 🧩 **P1: Kernspiel** | ❌ | S3 \- Kampf v1 | ❌ |  |
|  |  | S4 \- API | ❌ |  |
|  |  | S5 \- RNG | ❌ |  |
| 🐲 **P2: RPG-Tiefe** | ❌ | S7 \- RPG-Systeme | ❌ |  |
|  |  | S8 \- Kampf v2 | ❌ |  |
|  |  | S9 \- Gegner-KI | ❌ |  |
| 🌍 **P3: Welt** | ❌ | S10a \- Sammeln | ❌ |  |
|  |  | ... | ❌ |  |
| 🖥️ **P4: Politur** | ❌ | S15 \- Viewer | ❌ |  |
|  |  | S16 \- Qualität | ❌ |  |
| 🌳 **P5: Erweiterung** | ❌ | S17 \- Fraktionen | ❌ |  |
|  |  | ... | ❌ |  |
| 🤖 **P6: RL** | ❌ | S20 \- Simulation | ❌ |  |
|  |  | ... | ❌ |  |
| 🌳 **P7: Dynamik** | ❌ | S27 \- Director AI | ❌ |  |
|  |  | ... | ❌ |  |

