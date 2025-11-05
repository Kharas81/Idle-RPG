import os
import json5
from typing import Dict, Any

# Suche das Projekt-Root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
ITEMS_DIR = os.path.join(PROJECT_ROOT, 'config/items')

def load_all_items() -> Dict[str, Any]:
    items = {}
    if not os.path.isdir(ITEMS_DIR):
        raise FileNotFoundError(f"Item-Verzeichnis nicht gefunden: {ITEMS_DIR}")
    for filename in os.listdir(ITEMS_DIR):
        if filename.endswith('.json5'):
            path = os.path.join(ITEMS_DIR, filename)
            with open(path, 'r', encoding='utf-8') as f:
                data = json5.load(f)
                items.update(data)
    return items

# Beispielnutzung:
if __name__ == "__main__":
    all_items = load_all_items()
    print(f"Geladene Items: {len(all_items)}")
    print(list(all_items.keys()))
