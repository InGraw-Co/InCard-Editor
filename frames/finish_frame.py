# ================== BIBLIOTEKI ==================
import tkinter as tk
from tkinter import ttk
import json, os
from paths import *
from config import *


# ================== SESJA 4 ==================
class FinishFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        L = self.app.L

        ttk.Label(self, text=L["finish.title"],
                  font=("Segoe UI", 22)).pack(pady=60)

        ttk.Label(self, text=L["finish.saved"]).pack(pady=10)
        ttk.Button(self, text=L["finish.close"], command=self.finish).pack(pady=40)

    def finish(self):
        cards = {}

        with open(CARDS_TMP, "r", encoding="utf-8") as f:
            for line in f:
                obj = json.loads(line)
                cards[str(obj["id"])] = {
                    "n": obj["n"],
                    "r": obj["r"],
                    "t": obj["t"],
                    "p": obj["p"],
                    "a": obj["a"]
                }

        with open(os.path.join(CACHE_DIR, "cards.json"), "w", encoding="utf-8") as f:
            json.dump(cards, f, ensure_ascii=False, separators=(",", ":"))

        if os.path.exists(META_FILE):
            os.remove(META_FILE)
        if os.path.exists(CARDS_TMP):
            os.remove(CARDS_TMP)

        self.app.quit()
