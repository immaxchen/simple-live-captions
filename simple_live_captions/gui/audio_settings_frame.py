import customtkinter as ctk
import tkinter as tk
import soundcard as sc
import logging

class AudioSettingsFrame(ctk.CTkFrame):
    """Settings frame for audio-related configurations"""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.input_source_var = tk.StringVar()
        self.language_var = tk.StringVar()
        self.microphones = []
        self.microphone_dict = {}

        self._get_audio_devices()
        self._create_widgets()
        self._load_current_values()

    def _get_audio_devices(self):
        """Get available audio devices"""
        try:
            self.microphones = sc.all_microphones(include_loopback=True)
            self.microphone_dict = {mic.name: mic for mic in self.microphones}
            logging.info(f"Found {len(self.microphones)} audio devices")
        except Exception as e:
            logging.error(f"Error getting microphones: {e}")
            self.microphones = []
            self.microphone_dict = {}

    def _create_widgets(self):
        """Create all UI widgets"""
        self.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self, text="Input Source:", font=self.app.font).grid(
            row=1, column=0, padx=10, pady=5
        )

        mic_names = list(self.microphone_dict.keys()) or ["No microphones found"]
        self.mic_combo = ctk.CTkComboBox(
            self, width=400, font=self.app.font, values=mic_names,
            variable=self.input_source_var, command=self._on_mic_change, state="readonly"
        )
        self.mic_combo.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        ctk.CTkLabel(self, text="Language:", font=self.app.font).grid(
            row=2, column=0, padx=10, pady=5
        )

        languages = list(self.app.model_paths.keys())
        self.lang_combo = ctk.CTkComboBox(
            self, width=400, font=self.app.font, values=languages,
            variable=self.language_var, command=self._on_lang_change, state="readonly"
        )
        self.lang_combo.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

    def _load_current_values(self):
        """Load current app settings into the UI"""
        # Set microphone
        if (self.app.mic and hasattr(self.app.mic, 'name') and 
            self.app.mic.name in self.microphone_dict):
            self.input_source_var.set(self.app.mic.name)
        elif self.microphone_dict:
            first_mic = list(self.microphone_dict.keys())[0]
            if first_mic != "No microphones found":
                self.input_source_var.set(first_mic)

        # Set language
        if self.app.lang in self.app.model_paths:
            self.language_var.set(self.app.lang)
        elif self.app.model_paths:
            self.language_var.set(list(self.app.model_paths.keys())[0])

    def _stop_recording_if_active(self):
        """Stop recording if currently active"""
        if hasattr(self.app, 'is_recording') and self.app.is_recording:
            self.app.buttons.toggle_recording()

    def _on_mic_change(self, selected_name):
        """Handle microphone change"""
        try:
            selected_mic = self.microphone_dict.get(selected_name)
            self._stop_recording_if_active()
            self.app.mic = selected_mic
            logging.info(f"Changed microphone to: {selected_name}")
        except Exception as e:
            logging.error(f"Error changing microphone: {e}")

    def _on_lang_change(self, selected_language):
        """Handle language change"""
        try:
            self._stop_recording_if_active()
            self.app.lang = selected_language
            self.app._load_model()
            logging.info(f"Changed language to: {selected_language}")
        except Exception as e:
            logging.error(f"Error changing language: {e}")
