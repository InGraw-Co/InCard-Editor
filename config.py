# ================== BIBLIOTEKI ==================
import json, os, locale, sys
from tkinter import messagebox
from paths import *
import tkinter as tk


# ================= KONFIGURACJA OKNA ==================
def center_window(root, w=WIN_W, h=WIN_H):
    root.update_idletasks()
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")


# ================== SESJA KART ==================
def load_session_info():
    if not os.path.exists(CARDS_TMP):
        return 0
    last_id = 0
    with open(CARDS_TMP, "r", encoding="utf-8") as f:
        for line in f:
            try:
                last_id = json.loads(line).get("id", last_id)
            except:
                pass
    return last_id

def save_meta(total):
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump({"total": total}, f)

def load_meta():
    if not os.path.exists(META_FILE):
        return 0
    with open(META_FILE, "r", encoding="utf-8") as f:
        return json.load(f).get("total", 0)


# ================== USTAWIENIA APLIKACJI ==================
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_settings(data):
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ================== JĘZYK APLIKACJI ==================
def detect_system_lang():
    loc, _ = locale.getlocale()
    return (loc.split("_")[0] if loc else "en")

def get_available_languages():
    return sorted(f[:-5] for f in os.listdir(LANG_DIR) if f.endswith(".json"))

def load_language(code):
    path = os.path.join(LANG_DIR, f"{code}.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ================== KONFIGURACJA KART ==================
def load_config(L):
    if not os.path.exists(CONFIG_FILE):
        messagebox.showerror(L["error.config.title"], L["error.config.missing"])
        sys.exit()

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    return cfg["rarity"], cfg["types"], cfg["properties"]


# ================== WIDŻETY ==================
class RoundedButton(tk.Canvas):
    def __init__(
        self, parent, text, command,
        width=200, height=200,
        radius=25,
        bg="#d6d6d6",
        shadow="#5C5C5C",
        fg="#222",
        font=("Segoe UI", 16)
    ):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=parent["bg_color"] if hasattr(parent, "bg_color") else "#ececec",
            highlightthickness=0
        )

        self.command = command
        self.width = width
        self.height = height
        self.radius = radius

        self.shadow_rect = self._round_rect(6, 6, width, height, radius, fill=shadow, outline="")
        self.btn_rect = self._round_rect(0, 0, width-6, height-6, radius, fill=bg, outline="")
        self.text_id = self.create_text(
            (width-6)//2,
            (height-6)//2,
            text=text,
            fill=fg,
            font=font,
            justify="center"
        )

        self.bind("<Button-1>", lambda e: self.command())
        self.bind("<Enter>", self._hover)
        self.bind("<Leave>", self._leave)

    def _round_rect(self, x1, y1, x2, y2, r=25, **kwargs):
        points = [
            x1+r, y1,
            x2-r, y1,
            x2, y1,
            x2, y1+r,
            x2, y2-r,
            x2, y2,
            x2-r, y2,
            x1+r, y2,
            x1, y2,
            x1, y2-r,
            x1, y1+r,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _hover(self, e):
        self.move(self.btn_rect, 0, -2)
        self.move(self.text_id, 0, -2)

    def _leave(self, e):
        self.move(self.btn_rect, 0, 2)
        self.move(self.text_id, 0, 2)

    def set_colors(self, bg, fg, shadow=None):
        self.itemconfig(self.btn_rect, fill=bg)
        self.itemconfig(self.text_id, fill=fg)
        if shadow:
            self.itemconfig(self.shadow_rect, fill=shadow)

    def set_bg(self, bg):
        self.config(bg=bg)


# ================== POMOCNICZE FUNKCJE KOLORYSTYCZNE ==================
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb

def lerp(a, b, t):
    return int(a + (b - a) * t)

def lerp_color(c1, c2, t):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return rgb_to_hex((
        lerp(r1, r2, t),
        lerp(g1, g2, t),
        lerp(b1, b2, t)
    ))


# ================== KONFIGURACJA ==================

settings = load_settings()
lang = settings.get("lang") or detect_system_lang()
settings["lang"] = lang
theme = settings.get("theme") or "light"
settings["theme"] = theme
save_settings(settings)

L = load_language(lang)
RARITY, TYPES, PROPERTIES = load_config(L)