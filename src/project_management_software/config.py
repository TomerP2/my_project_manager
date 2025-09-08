# config.py
import json, os, sys

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path) # type: ignore
    return os.path.join(os.path.dirname(__file__), relative_path)

SETTINGS_PATH = resource_path("settings.json")

def load_settings():
    global settings
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        settings = json.load(f)

def save_settings():
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)

# Load once at startup
load_settings()