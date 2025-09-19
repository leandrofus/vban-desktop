import json
from pathlib import Path

CONFIG_FILE = Path.home() / ".vban_config.json"

DEFAULT_CONFIG = {
    "host": "10.10.0.2",
    "port": "6980",
    "stream": "Stream1",
    "vban_path": "/usr/local/bin/vban_receptor"
}

config = DEFAULT_CONFIG.copy()

def load_config():
    global config
    if CONFIG_FILE.exists():
        try:
            config.update(json.loads(CONFIG_FILE.read_text()))
        except Exception:
            config = DEFAULT_CONFIG.copy()
    return config

def save_config():
    CONFIG_FILE.write_text(json.dumps(config))