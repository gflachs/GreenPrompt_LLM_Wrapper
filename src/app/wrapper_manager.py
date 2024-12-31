import json
import os

def load_llm_config(config_path):
    """Loads the configuration from a JSON file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at {config_path}")

    with open(config_path, "r") as file:
        config = json.load(file)

    return config

