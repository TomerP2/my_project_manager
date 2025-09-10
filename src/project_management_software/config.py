# config.py
import json, os, sys

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path) # type: ignore
    return os.path.join(os.path.dirname(__file__), relative_path)

SETTINGS_PATH = resource_path("settings.json")

# Define the default settings
DEFAULT_SETTINGS = {
    "default projects folder": "./Projects",
    "default templates folder": "./template_folders",
    "default archive folder": "./Archive",
}

# Check if settings.json exists, if not, create it with default settings
if not os.path.exists(SETTINGS_PATH):
    with open(SETTINGS_PATH, 'w', encoding="utf-8") as settings_file:
        json.dump(DEFAULT_SETTINGS, settings_file, indent=2)

def load_settings():
    global settings
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        settings = json.load(f)

def save_settings():
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)

# Load once at startup
load_settings()