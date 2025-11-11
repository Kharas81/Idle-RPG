# RL-Grundgerüst für Idle-RPG

Dieses Modul stellt eine Gymnasium-kompatible RL-Umgebung bereit (`RpgEnv`), mit der KI-Agenten das Spiel trainieren können.

## Dateien
- `rpg_project/src/rl/environment.py`: Hauptumgebung
- `rpg_project/src/rl/spaces.py`: Spaces-Definitionen
- `config/rl_env.json5`: Konfiguration
- `tests/integration/test_rl_environment.py`: Integrationstest

## Schnellstart
```bash
pip install gymnasium pytest
pytest tests/integration/test_rl_environment.py
```
