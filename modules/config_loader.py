# /////////////////////////////////////////
# BY: Enes COBAN
# /////////////////////////////////////////

import yaml
from pathlib import Path

class ConfigLoader:
    @staticmethod
    def load_config(path: str) -> dict:
        config_path = Path(path)
        if not config_path.is_file():
            raise FileNotFoundError(f"Configuration file not found: {path}")
        with config_path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)