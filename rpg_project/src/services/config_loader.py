import json5
from pathlib import Path
from typing import Dict
from pydantic import ValidationError
from rpg_project.src.models.config_models import ItemConfig, OpponentConfig

class ConfigLoaderService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConfigLoaderService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.configs: Dict[str, Dict] = {}

    def load_configs(self, config_dir: str):
        for file_path in Path(config_dir).glob("*.json5"):
            with open(file_path, "r") as file:
                try:
                    self.configs[file_path.stem] = json5.load(file)
                except json5.JSONDecodeError as e:
                    print(f"Error decoding {file_path}: {e}")

    def get_item_config(self, item_id: str) -> ItemConfig:
        try:
            return ItemConfig(**self.configs["items"][item_id])
        except KeyError:
            raise ValueError(f"Item ID {item_id} not found in items config.")
        except ValidationError as e:
            print(f"Validation error for item {item_id}: {e}")

    def get_opponent_config(self, opponent_id: str) -> OpponentConfig:
        try:
            return OpponentConfig(**self.configs["opponents"][opponent_id])
        except KeyError:
            raise ValueError(f"Opponent ID {opponent_id} not found in opponents config.")
        except ValidationError as e:
            print(f"Validation error for opponent {opponent_id}: {e}")