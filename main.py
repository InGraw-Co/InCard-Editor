# ================== BIBLIOTEKI ==================
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

from paths import *
from config import *
from frames import WelcomeFrame, ConfigFrame, IntermediateFrame, EditorFrame, FinishFrame

# ================== APP ==================

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # === ŁADOWANIE USTAWIEŃ I JĘZYKA ===
        self.L = L
        self.rarity = RARITY
        self.types = TYPES
        self.properties = PROPERTIES
        self.theme = theme
        self.settings = settings

        self.theme = "light"
        self.bg_light = "#ececec"
        self.bg_dark = "#1b1b1b"

        self.fg_btn_light = "#2C2C2C"
        self.fg_btn_dark = "#E9E9E9"
        self.bg_btn_light = "#C0C0C0"
        self.bg_btn_dark = "#9B9B9B"

        self.title(L["app.title"])
        self.resizable(False, False)

        # === CENTROWANIE OKNA ===
        self.withdraw()        
        self.geometry(f"{WIN_W}x{WIN_H}")
        self.update_idletasks()

        w = self.winfo_width()
        h = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()

        x = (sw - w) // 2
        y = (sh - h) // 2

        self.geometry(f"+{x}+{y}")
        self.deiconify()

        # === MENU ===
        menubar = tk.Menu(self)

        lang_menu = tk.Menu(menubar, tearoff=0)
        self.available_langs = get_available_languages()
        for lc in self.available_langs:
            lang_menu.add_command(
                label=lc.upper(),
                command=lambda code=lc: self.change_language(code)
            )

        menubar.add_cascade(
            label=L.get("menu.language", "Language"),
            menu=lang_menu
        )

        menubar.add_command(
            label=L["menu.advanced"],
            command=self.advanced_action
        )

        menubar.add_command(
            label=L["menu.info"],
            command=self.show_info
        )

        self.config(menu=menubar)

        # === INICJALIZACJA ZMIENNYCH ===
        self.cards_total = 0
        self.current_id = 1
        self.current_frame_name = None

        # === KONTENER NA FRAME'Y ===
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (WelcomeFrame, IntermediateFrame, EditorFrame, FinishFrame, ConfigFrame):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.place(relwidth=1, relheight=1)

        self.show("WelcomeFrame")

        # ====== IKONA APLIKACJI ======
        try:
            self.icon_image = tk.PhotoImage(file=ICON)
            self.iconphoto(True, self.icon_image)
        except Exception as e:
            print(f"Nie udało się wczytać ikony: {e}")
        

    # ================== ZARZĄDZANIE FRAME'AMI ==================
    def show(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
        self.current_frame_name = frame_name
        print_info(frame_name)
        if hasattr(frame, "on_show"):
            frame.on_show()
            print(f"Funckja on_show() w {frame_name} została wywołana.")



    # ================== AKCJE MENU ==================
    def advanced_action(self):
        current_frame = self.frames.get(self.current_frame_name)
        print(f"Aktualny frame: {self.current_frame_name}")
        if isinstance(current_frame, EditorFrame):
            current_frame.show_advanced_window()
        else:
            messagebox.showinfo(
                self.L["menu.advanced"],
                self.L["advanced.unavailable"]
            )

    def show_info(self):
        messagebox.showinfo(
            self.L["menu.info"],
            self.L["info.text"]
        )

    def change_language(self, lang_code):
        """Zapisuje język i restartuje aplikację"""
        settings["lang"] = lang_code
        save_settings(settings)
        messagebox.showinfo(
            self.L["lang.info"],
            self.L["lang.restart"]
        )
        self.destroy()
        os.execl(sys.executable, sys.executable, *sys.argv)


# ================== START ==================
if __name__ == "__main__":
    App().mainloop()
