import customtkinter as ctk
import soundcard as sc
import logging
from simple_live_captions.core.recognizer import SpeechRecognizer
from simple_live_captions.gui.buttons_frame import ButtonsFrame

class SimpleLiveCaptionsApp(ctk.CTk):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.title("Simple Live Captions")
        self.resizable(True, False)
        self.attributes("-topmost", True)

        self.font = tuple(config["ui_fonts"])
        self.lang = config["default_audio_language"]
        self.model_paths = config["model_paths"]

        self.mic = None
        self.recognizer = None
        self.accept_index = "1.0"
        self.is_recording = False

        self._setup_ui()
        self._center_bottom_window()
        self._initialize_audio()

    def _setup_ui(self):
        """Setup the UI components"""
        self.grid_columnconfigure(0, weight=1)

        self.textbox = ctk.CTkTextbox(self, width=self.config["textbox_width"],
                                      height=self.config["textbox_height"],
                                      font=tuple(self.config["textbox_font"]), wrap="word")
        self.textbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.buttons = ButtonsFrame(self)
        self.buttons.grid(row=0, column=1, padx=5, pady=5, sticky="n")

    def _center_bottom_window(self):
        """Position window at middle bottom of screen"""
        self.update_idletasks()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()

        x = (screen_width - window_width) // 2
        y = screen_height - window_height - 75  # px from bottom

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def _show_error(self, message):
        """Show error message in the textbox"""
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", f"ERROR: {message}")

    def _initialize_audio(self):
        """Initialize audio components"""
        try:
            default_speaker = sc.default_speaker()
            if default_speaker:
                self.mic = sc.get_microphone(id=default_speaker.id, include_loopback=True)
            else:
                mics = sc.all_microphones(include_loopback=True)
                if mics:
                    self.mic = mics[0]
                else:
                    raise Exception("No microphones available")

            self._load_model()

        except Exception as e:
            logging.error(f"Failed to initialize audio: {e}")
            self._show_error("Failed to initialize audio system. Please check your audio devices.")

    def _load_model(self):
        """Load the speech recognition model"""
        try:
            model_path = self.model_paths.get(self.lang)
            if not model_path:
                raise Exception(f"No model path configured for language: {self.lang}")

            self.recognizer = SpeechRecognizer(self.config, model_path, self.mic, self._on_result_safe)

        except Exception as e:
            logging.error(f"Failed to load model: {e}")
            self._show_error(f"Failed to load speech model for {self.lang}. Please check model files.")

    def _on_result_safe(self, text, is_final):
        """Thread-safe wrapper for handling recognition results"""
        self.after(0, lambda: self._on_result(text, is_final))

    def _on_result(self, text, is_final):
        """Handle recognition results"""
        try:
            is_last_char_visible= self.textbox.bbox("end-1c")
            self.textbox.delete(self.accept_index, "end")
            self.textbox.insert("end", "\n" + text)
            if is_final:
                self.accept_index = self.textbox.index("end")
            if is_last_char_visible:
                self.textbox.see("end")
        except Exception as e:
            logging.error(f"Error updating textbox: {e}")

    def toggle_recording(self):
        """Toggle recording state"""
        try:
            if self.is_recording:
                self.recognizer.stop()
                self.is_recording = False
                return False
            else:
                self.recognizer.start()
                self.is_recording = True
                return True
        except Exception as e:
            logging.error(f"Error toggling recording: {e}")
            self._show_error(f"Failed to toggle recording: {e}")
            self.is_recording = False
            return False
