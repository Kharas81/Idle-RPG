import os
import json5
from collections import defaultdict

# Pfade
ITEMS_JSON5 = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config/items.json5'))
ITEMS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config/items'))

# Mapping: Item-Typ zu Zieldatei
TYPE_TO_FILE = {
    'weapon': 'weapons.json5',
    'armor': 'armor.json5',
    'accessory': 'accessories.json5',
    'consumable': 'consumables.json5',
    'resource': 'resources.json5',
    'quest': 'quest_items.json5',
    'trade_good': 'trade_goods.json5',
}

def main():
    with open(ITEMS_JSON5, 'r', encoding='utf-8') as f:
        all_items = json5.load(f)

    # Items nach Typ sortieren
    items_by_type = defaultdict(dict)
    for item_id, item in all_items.items():
        item_type = item.get('type')
        target_file = TYPE_TO_FILE.get(item_type)
        if target_file:
            items_by_type[target_file][item_id] = item
        else:
            print(f"Unbekannter Typ: {item_type} für Item {item_id}")

    # Schreibe die Dateien
    for filename, items in items_by_type.items():
        path = os.path.join(ITEMS_DIR, filename)
        with open(path, 'w', encoding='utf-8') as f:
            json5.dump(items, f, ensure_ascii=False, indent=2)
        print(f"{len(items)} Items nach {filename} geschrieben.")

if __name__ == "__main__":
    main()
