import numpy as np
import json
import threading
import logging
from vosk import Model, KaldiRecognizer, SetLogLevel

class SpeechRecognizer:
    def __init__(self, config, model_path, mic, on_result):
        self.sample_rate = config["sample_rate"]
        self.buffer_size = config["buffer_size"]
        self.chunk_size = config["chunk_size"]
        self.partial_interval = config["partial_result_interval"]
        self.mic = mic
        self.on_result = on_result
        self.recording = False

        if config.get("enable_logging", True):
            SetLogLevel(0)
        else:
            SetLogLevel(-1)

        try:
            self.model = Model(model_path)
            logging.info(f"Successfully loaded model from {model_path}")
        except Exception as e:
            logging.error(f"Failed to load model from {model_path}: {e}")
            raise RuntimeError(f"Could not load speech recognition model: {e}")

    def start(self):
        """Start speech recognition"""
        if self.recording:
            logging.warning("Recording already in progress")
            return

        self.recording = True
        threading.Thread(target=self._recognize_loop, daemon=True).start()
        logging.info("Speech recognition started")

    def stop(self):
        """Stop speech recognition"""
        if not self.recording:
            logging.warning("Recording already stopped")
            return

        self.recording = False
        logging.info("Speech recognition stopped")

    def _recognize_loop(self):
        """Main recognition loop"""
        try:
            recognizer = KaldiRecognizer(self.model, self.sample_rate)
            partial_count = 0

            with self.mic.recorder(samplerate=self.sample_rate, channels=[0], blocksize=self.buffer_size) as recorder:
                while self.recording:
                    audio = recorder.record(numframes=self.chunk_size)

                    if audio.ndim > 1:
                        audio = np.mean(audio, axis=1)

                    audio_bytes = np.int16(audio * 32767).tobytes()

                    if recognizer.AcceptWaveform(audio_bytes):
                        text = json.loads(recognizer.Result()).get("text", "")
                        if text.strip():
                            self.on_result(text, is_final=True)
                        partial_count = 0

                    elif partial_count % self.partial_interval == 0:
                        text = json.loads(recognizer.PartialResult()).get("partial", "")
                        if text.strip():
                            self.on_result(text, is_final=False)
                        partial_count = 0

                    partial_count += 1

        except Exception as e:
            logging.error(f"Critical error in recognition loop: {e}")

        finally:
            self.recording = False
            logging.info("Recognition loop ended")
