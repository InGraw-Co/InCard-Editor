# ================== BIBLIOTEKI ==================
import os

# ================== PODSTAWOWE ŚCIEŻKI ==================
WIN_W, WIN_H = 1300, 1000
ICON_SIZE = 512

SETTINGS_FILE = "settings/settings.json"
LANG_DIR = "settings/lang"
CONFIG_FILE = "config.json"

CACHE_DIR = "cache"
ICON_DIR = os.path.join(CACHE_DIR, "icons")
CARDS_TMP = os.path.join(CACHE_DIR, "cards.ndjson")
META_FILE = os.path.join(CACHE_DIR, "cards.meta.json")

os.makedirs(ICON_DIR, exist_ok=True)