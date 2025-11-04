from pathlib import Path
from typing import TypeVar

import json5

T = TypeVar("T")

class ConfigLoader:
    @staticmethod
    def load_config(path: str, model: type[T]) -> list[T]:
        from pydantic import TypeAdapter
        file_path = Path(path)
        with file_path.open("r", encoding="utf-8") as f:
            data = json5.load(f)
        # Falls data ein Dict ist (wie bei talents), Werte extrahieren
        if isinstance(data, dict):
            data = list(data.values())
        adapter = TypeAdapter(list[model])
        return adapter.validate_python(data)
