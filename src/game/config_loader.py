import json
import os

import toml
import yaml


class ConfigLoader:
    @staticmethod
    def load_config(path):
        ext = os.path.splitext(path)[1].lower()
        with open(path, 'r', encoding='utf-8') as f:
            if ext in ['.yaml', '.yml']:
                return yaml.safe_load(f)
            elif ext == '.json':
                return json.load(f)
            elif ext == '.toml':
                return toml.load(f)
            else:
                raise ValueError(f"Unsupported config file type: {ext}")
