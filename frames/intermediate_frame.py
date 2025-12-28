# ================== BIBLIOTEKI ==================
import tkinter as tk
from tkinter import ttk
import os, shutil
from paths import *
from config import *

# ================== SESJA 2 ==================
class IntermediateFrame(ttk.Frame):
    BUTTON_SIZE = 200

    # ================== INICJALIZACJA ==================
    def __init__(self, parent, app):
        super().__init__(parent)

        # ================== ZMIENNE ==================
        self.app = app
        settings = load_settings()
        self.settings = app.settings
        current_theme = settings.get("theme", "light")
        self.current_theme = current_theme
        L = self.app.L

        self.animating = False

        # ================== TŁO ==================
        self.configure(padding=20)
        self.style = ttk.Style()
        self.style.configure("Intermediate.TFrame", background=self.app.bg_light)
        self.configure(style="Intermediate.TFrame")

        # ================== TYTUŁ ==================
        self.title_lbl = ttk.Label(
            self,
            text=L["intermediate.title"],
            font=("Segoe UI", 24)
        )
        self.title_lbl.pack(pady=(40, 60))
        self.style.configure(
            "IntermediateTitle.TLabel",
            background=self.app.bg_light,
            foreground=self.app.fg_btn_light
        )
        self.title_lbl.configure(style="IntermediateTitle.TLabel")

        # ================== ENTRY LICZBY KART ==================
        self.entry_lbl = ttk.Label(
            self,
            text=L["intermediate.enter_cards"],
            font=("Segoe UI", 14)
        )
        self.entry_lbl.pack(pady=(0, 10))
        self.style.configure(
            "IntermediateEntry.TLabel",
            background=self.app.bg_light,
            foreground=self.app.fg_btn_light
        )
        self.entry_lbl.configure(style="IntermediateEntry.TLabel")

        self.cards_entry = ttk.Entry(self, font=("Segoe UI", 14), width=10, justify="center")
        self.cards_entry.pack(pady=(0, 30))
        self.cards_entry.insert(0, "10")

        # ================== PRZYCISK: DALEJ ==================
        self.next_btn = ttk.Button(
            self,
            text=L["intermediate.next"],
            command=self.start_new_session,
            width=20
        )
        self.next_btn.pack(pady=10)

        # ================== DARK MODE BUTTON ==================
        self.theme_btn = tk.Label(
            self,
            text="🌙",
            font=("Segoe UI", 14),
            bg=self.app.bg_light,
            fg=self.app.fg_btn_light,
            cursor="hand2"
        )
        self.theme_btn.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")
        self.theme_btn.bind("<Button-1>", lambda e: self.toggle_theme())

        # ================== INFO ==================
        self.info_lbl = ttk.Label(
            self,
            text="",
            foreground="#f5a623",
            font=("Segoe UI", 11)
        )
        self.info_lbl.pack(pady=20)
        self.style.configure("IntermediateInfo.TLabel",
                             background=self.app.bg_light, foreground="#f5a623")
        self.info_lbl.configure(style="IntermediateInfo.TLabel")

        # ============ USTAWIENIE MOTYWU ============
        if current_theme == "dark":
            self.theme_btn.config(text="☀")
            self.animate_theme(
                self.app.bg_btn_light, self.app.bg_btn_dark,
                self.app.fg_btn_light, self.app.fg_btn_dark,
                self.app.bg_light, self.app.bg_dark,
                step=30
            )
        else:
            self.theme_btn.config(text="🌙")
            self.animate_theme(
                self.app.bg_btn_dark, self.app.bg_btn_light,
                self.app.fg_btn_dark, self.app.fg_btn_light,
                self.app.bg_dark, self.app.bg_light,
                step=30
            )


    # ================== DARK MODE ==================
    def toggle_theme(self):
        if self.animating:
            return  
        
        self.animating = True

        if self.current_theme == "light":
            print("switch to dark")
            self.app.theme = "dark"
            self.settings["theme"] = "dark"
            save_settings(self.settings)
            current_theme = self.settings.get("theme", "light")
            print(current_theme)
            self.current_theme = "dark"  
            self.theme_btn.config(text="☀")
            self.animate_theme(
                self.app.bg_btn_light, self.app.bg_btn_dark,
                self.app.fg_btn_light, self.app.fg_btn_dark,
                self.app.bg_light, self.app.bg_dark
            )
        else:
            print("switch to light")
            self.app.theme = "light"
            self.settings["theme"] = "light"
            save_settings(self.settings)
            current_theme = self.settings.get("theme", "light")
            print(current_theme)
            self.current_theme = "light"  
            self.theme_btn.config(text="🌙")
            self.animate_theme(
                self.app.bg_btn_dark, self.app.bg_btn_light,
                self.app.fg_btn_dark, self.app.fg_btn_light,
                self.app.bg_dark, self.app.bg_light
            )

    # ================== ANIMACJA MOTYWU ==================
    def animate_theme(self, bg_from, bg_to, fg_from, fg_to, bg_theme_f, bg_theme_t, step=0):
        steps = 30
        t = step / steps

        bgt = lerp_color(bg_theme_f, bg_theme_t, t)
        bg = lerp_color(bg_from, bg_to, t)
        fg = lerp_color(fg_from, fg_to, t)

        self.style.configure("Intermediate.TFrame", background=bgt)
        self.style.configure("IntermediateTitle.TLabel", background=bgt, foreground=fg)
        self.style.configure("IntermediateEntry.TLabel", background=bgt, foreground=fg)
        self.style.configure("IntermediateInfo.TLabel", background=bgt)

        self.theme_btn.config(bg=bgt, fg=fg)
        self.info_lbl.config(background=bgt, foreground="#f5a623")
        self.entry_lbl.config(background=bgt, foreground=fg)

        if step < steps:
            self.after(16, lambda: self.animate_theme(
                bg_from, bg_to, fg_from, fg_to, bg_theme_f, bg_theme_t, step + 1
            ))
        else:
            self.animating = False

    # ================== START NOWEJ SESJI ==================
    def start_new_session(self):
        L = self.app.L
        try:
            total = int(self.cards_entry.get())
            if not (1 <= total <= 999):
                raise ValueError

            # ================== RESET SESJI ==================
            if os.path.exists(CARDS_TMP):
                os.remove(CARDS_TMP)
            if os.path.exists(META_FILE):
                os.remove(META_FILE)
            if os.path.exists(ICON_DIR):
                shutil.rmtree(ICON_DIR)
            os.makedirs(ICON_DIR, exist_ok=True)

            self.app.cards_total = total
            save_meta(total)

            self.app.show("EditorFrame")

        except Exception:
            self.info_lbl.config(
                text=L["welcome.error.invalid"],
                foreground="#f5a623"
            )

    # ================== MOTYW ==================
    def on_show(self):
        current_theme = self.settings.get("theme", "light")
        self.current_theme = current_theme

        if current_theme == "dark":
            self.theme_btn.config(text="☀")
            print("dark")
            self.animate_theme(
                self.app.bg_btn_light, self.app.bg_btn_dark,
                self.app.fg_btn_light, self.app.fg_btn_dark,
                self.app.bg_light, self.app.bg_dark,
                step=30
            )
        else:
            self.theme_btn.config(text="🌙")
            print("light")
            self.animate_theme(
                self.app.bg_btn_dark, self.app.bg_btn_light,
                self.app.fg_btn_dark, self.app.fg_btn_light,
                self.app.bg_dark, self.app.bg_light,
                step=30
            )
