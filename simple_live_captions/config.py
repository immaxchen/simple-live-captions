import json
import os
import logging

def load_config(path="config.json"):
    """Load configuration with validation"""
    if not os.path.exists(path):
        logging.info(f"Configuration file not found: {path}. Creating default configuration.")
        config = create_default_config()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        logging.info(f"Default configuration saved to {path}")
    else:
        try:
            with open(path, encoding="utf-8") as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in config file: {e}")
            raise

    validated_config = validate_config(config)
    logging.info(f"Configuration loaded successfully from {path}")
    return validated_config

def create_default_config():
    """Create a default configuration dictionary"""
    return {
        "enable_logging": True,
        "default_audio_language": "Japanese",
        "model_paths": {
            "English": "models/vosk-model-en-us-0.22",
            "Chinese": "models/vosk-model-cn-0.22",
            "Japanese": "models/vosk-model-ja-0.22",
        },
        "sample_rate": 16000,
        "buffer_size": 16000,
        "chunk_size": 3200,
        "partial_result_interval": 5,
        "ui_fonts": ["Segoe UI", 15],
        "textbox_font": ["メイリオ", 14],
        "textbox_width": 700,
        "textbox_height": 60,
    }

def validate_config(config):
    """Validate and set defaults for configuration values"""
    defaults = create_default_config()
    validated = config.copy()

    def validate_positive_int(key):
        if key not in validated or not isinstance(validated[key], int) or validated[key] <= 0:
            logging.warning(f"Invalid or missing {key}, using default")
            validated[key] = defaults[key]

    for key in ["sample_rate", "buffer_size", "chunk_size", "partial_result_interval", "textbox_width", "textbox_height"]:
        validate_positive_int(key)

    for key in ["ui_fonts", "textbox_font"]:
        if key not in validated or not isinstance(validated[key], list) or len(validated[key]) < 2:
            logging.warning(f"Invalid or missing {key}, using default")
            validated[key] = defaults[key].copy()

    if "model_paths" not in validated or not isinstance(validated["model_paths"], dict) or not validated["model_paths"]:
        logging.warning("Invalid or missing model_paths, using default")
        validated["model_paths"] = defaults["model_paths"].copy()

    existing_models = {lang: path for lang, path in validated["model_paths"].items() if os.path.exists(path)}
    missing_models = {lang: path for lang, path in validated["model_paths"].items() if lang not in existing_models}

    if missing_models:
        logging.warning(f"Missing model files: {', '.join(f'{k}: {v}' for k, v in missing_models.items())}")

    if not existing_models:
        logging.critical("No valid model files found. Application cannot continue.")
        raise RuntimeError("Fatal error: No available speech recognition models.")

    validated["model_paths"] = existing_models

    if "default_audio_language" not in validated:
        logging.warning(f"Invalid or missing default language, using default")
        validated["default_audio_language"] = defaults["default_audio_language"]

    if validated["default_audio_language"] not in validated["model_paths"]:
        fallback = next(iter(validated["model_paths"]))
        logging.warning(f"Default language '{validated['default_audio_language']}' not available, using '{fallback}'")
        validated["default_audio_language"] = fallback

    if "enable_logging" not in validated or not isinstance(validated["enable_logging"], bool):
        logging.warning(f"Invalid or missing enable_logging, using default")
        validated["enable_logging"] = defaults["enable_logging"]

    return validated
