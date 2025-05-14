import json
import os
import sys

try:
    from .constants import DEFAULT_SORT_ORDER
except ImportError:
    print("⚠️ Could not import constants for default sort order. Using fallback.")
    DEFAULT_SORT_ORDER = "last_modified"

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    full_path = os.path.join(base_path, relative_path)
    return os.path.normpath(full_path)

def load_config():
    config_file_name = "config.json"
    config_path = resource_path(config_file_name)

    print(f"DEBUG: Attempting to load config from path: {config_path}")

    default_config = {
        "DISCORD_BOT_TOKEN": "",
        "DISCORD_BOT_INVITE": "",
        "EFEITOS_DIR": "efeitos",
        "EMOJIS_DIR": "emojis",
        "VAR_ORDER": DEFAULT_SORT_ORDER,
        "VAR_TIME_LIMIT_EFFECT": 5
    }

    if not os.path.exists(config_path):
        print(f"🚫 config.json not found at {config_path}")
        return default_config, config_path

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)

        config_data.setdefault("DISCORD_BOT_TOKEN", "")
        config_data.setdefault("DISCORD_BOT_INVITE", "")
        config_data.setdefault("EFEITOS_DIR", "efeitos")
        config_data.setdefault("EMOJIS_DIR", "emojis")
        config_data.setdefault("VAR_ORDER", DEFAULT_SORT_ORDER)
        config_data.setdefault("VAR_TIME_LIMIT_EFFECT", 5)

        print(f"✅ Configuration loaded from: {config_path}")
        return config_data, config_path
    except json.JSONDecodeError as e:
        print(f"❌ Error decoding config.json at {config_path}: {e}")
        print("Using default configuration.")
        return default_config, config_path
    except Exception as e:
        print(f"❌ An unexpected error occurred loading config.json from {config_path}: {e}")
        print("Using default configuration.")
        return default_config, config_path

def save_config(config_data, config_path):
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"❌ Error saving config.json to {config_path}: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred saving config.json to {config_path}: {e}")