import customtkinter as ctk
import logging
from simple_live_captions.gui.audio_settings_frame import AudioSettingsFrame

class SettingsWindow(ctk.CTkToplevel):
    """Main settings window"""

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Settings")
        self.resizable(True, False)
        self.attributes('-topmost', True)

        try:
            self._setup_ui()
            self._center_window()
        except Exception as e:
            logging.error(f"Error creating settings window: {e}")

    def _setup_ui(self):
        """Setup the settings window UI"""
        self.grid_columnconfigure(0, weight=1)

        self.audio_settings = AudioSettingsFrame(self, self.app)
        self.audio_settings.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    def _center_window(self):
        """Position window at center of screen"""
        self.update_idletasks()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
