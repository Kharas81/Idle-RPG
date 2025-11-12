# Google Colab Setup & Test-Guide für Idle-RPG

## Ziel

- Projekt in Google Colab ausführen und testen
- RL-Agenten trainieren
- Frontend über ngrok bereitstellen und live testen

---

## 1. Projekt nach Colab & Drive kopieren

**A. Repository klonen**
```python
!git clone https://github.com/Kharas81/Idle-RPG.git
```

**B. Google Drive einbinden**
```python
from google.colab import drive
drive.mount('/content/drive')
```

**C. Arbeitsverzeichnis setzen**
```python
%cd /content/Idle-RPG
```

---

## 2. Abhängigkeiten installieren

```python
!pip install -r requirements.txt
!pip install gymnasium fastapi uvicorn ngrok
```

---

## 3. Tests ausführen

```python
!pytest --maxfail=1 --disable-warnings -v
```

---

## 4. RL-Agenten trainieren

**Beispiel: Explorer-Agent**
```python
!python scripts/train_explorer.py
```

**Beispiel: Fighter-Agent**
```python
!python scripts/train_fighter.py
```

---

## 5. Backend & Frontend starten (FastAPI + ngrok)

**A. Backend starten**
```python
!uvicorn rpg_project.src.main:app --host 0.0.0.0 --port 8000
```

**B. ngrok Tunnel öffnen**
```python
!ngrok authtoken <DEIN_NGROK_TOKEN>
!ngrok http 8000
```

**C. Frontend öffnen**
- Öffne `frontend/frontend_tester.html` oder `frontend/viewer.html` in Colab/Drive
- Trage die ngrok-URL als API-Endpunkt ein

---

## 6. KI-Entscheidungen im Frontend sichtbar machen

- Das Frontend zeigt den aktuellen Spielzustand und die Aktionen der KI-Agenten
- RL-Agenten können über die API gesteuert und beobachtet werden
- Für Live-Visualisierung: `viewer.html` verwenden
- **Tipp:** Im `viewer.html` werden die Positionen und Aktionen der Agenten als Emojis oder Icons dargestellt. Die Log-Ausgabe der KI-Entscheidungen kann als Text unter der Karte angezeigt werden.
- **Debug-Panel:** Richte im Frontend einen Bereich ein, der die letzten KI-Aktionen, Rewards und States anzeigt (z. B. als Liste oder Konsole).
- **ngrok-URL:** Nach dem Start von ngrok erhältst du eine URL wie `https://1234-xx-xx-xx-xx.ngrok.io`. Trage diese im Frontend als API-Endpunkt ein, damit die Verbindung zum Backend funktioniert.
- **Live-Reload:** Optional kannst du das Frontend so erweitern, dass es den Spielzustand regelmäßig abfragt (Polling) oder per WebSocket aktualisiert.

---

## Hinweise
- Alle Konfigurationsdateien (Items, Gegner, Skills, etc.) sind im `config`-Ordner
- RL-Umgebung und Agenten sind in `rpg_project/src/rl/` und `scripts/`
- Tests und Beispielskripte sind in `tests/` und `scripts/`
- Für eigene Experimente: Notebook-Zellen mit `%%writefile` und `!python` nutzen

---

## Troubleshooting
- Bei Import-Fehlern: Arbeitsverzeichnis prüfen (`%cd /content/Idle-RPG`)
- Bei Port-Problemen: ngrok-URL neu generieren
- Für Performance: Colab-Runtime auf GPU/TPU umstellen (optional)

---

Viel Erfolg beim Testen und Präsentieren in Colab!
