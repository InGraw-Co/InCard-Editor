# ================== BIBLIOTEKI ==================
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from paths import *
from config import *

# =================== SESJA 1 ==================
class WelcomeFrame(ttk.Frame):
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

        # ================== TŁO ==================
        self.configure(padding=20)
        self.style = ttk.Style()
        self.style.configure(
            "Welcome.TFrame",
            background=self.app.bg_light
        )
        self.configure(style="Welcome.TFrame")

        # ================== TYTUŁ ==================
        self.title_lbl = ttk.Label(
            self,
            text=L["welcome.title"],
            font=("Segoe UI", 24)
        )
        self.title_lbl.pack(pady=(40, 60))
        self.style.configure(
            "WelcomeTitle.TLabel",
            background=self.app.bg_light,
            foreground=self.app.fg_btn_light
        )
        self.title_lbl.configure(style="WelcomeTitle.TLabel")
        self.animating = False

        # ================== KONTENER PRZYCISKÓW ==================
        self.style.configure(
            "WelcomeButtons.TFrame",
            background=self.app.bg_light
        )
        self.button_frame = ttk.Frame(
            self,
            style="WelcomeButtons.TFrame"
        )
        self.button_frame.pack()

        # ================== PRZYCISK: NOWY ==================
        self.new_btn = RoundedButton(
            self.button_frame,
            text=L["welcome.new_project"],
            command=lambda: self.app.show("IntermediateFrame"),
            width=self.BUTTON_SIZE,
            height=self.BUTTON_SIZE
        )
        self.new_btn.grid(row=0, column=0, padx=40)

        # ================== PRZYCISK: WCZYTAJ ==================
        self.load_btn = RoundedButton(
            self.button_frame,
            text=L["welcome.load_project"],
            command=self.load_project,
            width=self.BUTTON_SIZE,
            height=self.BUTTON_SIZE
        )
        self.load_btn.grid(row=0, column=1, padx=40)

        # ================== PRZYCISK: PRZYWRÓĆ PROJEKT ==================
        self.restore_btn = RoundedButton(
            self.button_frame,
            text=L["welcome.restore"],
            command=self.restore_project,
            width=440,
            height=60
        )
        self.restore_btn.grid(row=1, column=0, columnspan=2, pady=20)

        # ================== PRZYCISK: KONFIGURACJA ==================
        self.config_btn = RoundedButton(
            self.button_frame,
            text=L["welcome.config"],
            command=lambda: self.app.show("ConfigFrame"),
            width=440,
            height=60
        )
        self.config_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # ================== INFO O SESJI ==================
        self.session_info = ttk.Label(
            self,
            text="",
            foreground="#f5a623",
            font=("Segoe UI", 11)
        )
        self.session_info.pack(pady=30)
        self.style.configure(
            "WelcomeInfo.TLabel",
            background=self.app.bg_light,
            foreground="#f5a623"
        )
        self.session_info.configure(style="WelcomeInfo.TLabel")

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

        # ================== SPRAWDŹ POPRZEDNIĄ SESJĘ ==================
        last_id = load_session_info()
        if last_id > 0:
            total_saved = load_meta()
            self.session_info.config(
                text=L["welcome.session_detected"].format(
                    saved=last_id,
                    total=total_saved
                )
            )

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

        self.style.configure("Welcome.TFrame", background=bgt)
        self.style.configure("WelcomeButtons.TFrame", background=bgt)
        self.style.configure("WelcomeTitle.TLabel", background=bgt, foreground=fg)
        self.style.configure("WelcomeInfo.TLabel", background=bgt)

        self.theme_btn.config(bg=bgt, fg=fg)
        self.session_info.config(background=bgt, foreground="#f5a623")

        for btn in (self.load_btn, self.new_btn, self.restore_btn, self.config_btn):
            btn.set_colors(bg, fg)
            btn.set_bg(bgt)

        if step < steps:
            self.after(16, lambda: self.animate_theme(
                bg_from, bg_to, fg_from, fg_to, bg_theme_f, bg_theme_t, step + 1
            ))
        else:
            self.animating = False

    # =================== WCZYTYWANIE PROJEKTU ==================
    def load_project(self):
        folder = filedialog.askdirectory(title=L["project.catolog"])
        if not folder:
            return

        json_file = os.path.join(folder, "cards.json")
        icons_folder = os.path.join(folder, "icons")

        if not os.path.isfile(json_file):
            self.session_info.config(text=L["error.cards.invalid"], foreground="#ffa600")
            return
        if not os.path.isdir(icons_folder):
            self.session_info.config(text=L["error.icons.invalid"], foreground="#ffa600")
            return
        png_files = [f for f in os.listdir(icons_folder) if f.lower().endswith(".png")]
        if not png_files:
            self.session_info.config(text=L["error.pngs.invalid"], foreground="#ffa600")
            return

        self.session_info.config(text=L["project.loaded"], foreground="#00cc00")
        messagebox.showinfo(L["finish.title"], L["project.loaded"])

    # =================== PRZYWRACANIE PROJEKTU ==================
    def restore_project(self):
        cache_folder = os.path.join(os.getcwd(), "cache")
        ndjson_file = os.path.join(cache_folder, "cards.ndjson")
        meta_file = os.path.join(cache_folder, "cards.meta.json")
        icons_folder = os.path.join(cache_folder, "icons")

        if not os.path.isdir(cache_folder):
            self.session_info.config(text=L["error.cache.invalid"], foreground="#ffa600")
            return
        if not os.path.isfile(ndjson_file):
            self.session_info.config(text=L["error.cards.nd.invalid"], foreground="#ffa600")
            return
        if not os.path.isfile(meta_file):
            self.session_info.config(text=L["error.cards.meta.invalid"], foreground="#ffa600")
            return
        if not os.path.isdir(icons_folder):
            self.session_info.config(text=L["error.icons.invalid"], foreground="#ffa600")
            return
        png_files = [f for f in os.listdir(icons_folder) if f.lower().endswith(".png")]
        if not png_files:
            self.session_info.config(text=L["error.pngs.invalid"], foreground="#ffa600")
            return

        self.app.current_id = load_session_info() + 1
        self.app.cards_total = load_meta()

        self.app.show("EditorFrame")

    # =================== KONFIGURACJA ==================
    def open_config(self):
        messagebox.showinfo(L["config.title"], "Tutaj możesz dodać swoją konfigurację")
