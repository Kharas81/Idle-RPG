import json5
from pathlib import Path
from typing import Type, TypeVar, List
from pydantic import parse_obj_as

T = TypeVar("T")

class ConfigLoader:
    @staticmethod
    def load_config(path: str, model: Type[T]) -> List[T]:
        from pydantic import TypeAdapter
        file_path = Path(path)
        with file_path.open("r", encoding="utf-8") as f:
            data = json5.load(f)
        adapter = TypeAdapter(List[model])
        return adapter.validate_python(data)
