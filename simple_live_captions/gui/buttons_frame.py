import customtkinter as ctk
import logging
from simple_live_captions.gui.settings_window import SettingsWindow

class ButtonsFrame(ctk.CTkFrame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.configure(fg_color="transparent")

        self.record_btn = ctk.CTkButton(
            self, 
            width=30, 
            height=30, 
            font=self.app.font, 
            text='🎧',
            command=self.toggle_recording
        )
        self.record_btn.grid(row=0, column=0, padx=5, pady=5)

        self.settings_btn = ctk.CTkButton(
            self, 
            width=30, 
            height=30, 
            font=self.app.font, 
            text='⚙️',
            command=self.open_settings
        )
        self.settings_btn.grid(row=1, column=0, padx=5, pady=5)

    def toggle_recording(self):
        """Toggle recording and update button state"""
        try:
            recording = self.app.toggle_recording()
            self.record_btn.configure(text="⏸️" if recording else "🎧")
        except Exception as e:
            logging.error(f"Error toggling recording: {e}")

    def open_settings(self):
        """Open settings window"""
        try:
            if not hasattr(self.app, "settings_window") or not self.app.settings_window.winfo_exists():
                self.app.settings_window = SettingsWindow(self.app)
            else:
                self.app.settings_window.focus()
        except Exception as e:
            logging.error(f"Error opening settings: {e}")
