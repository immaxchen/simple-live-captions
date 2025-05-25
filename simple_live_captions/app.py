import logging
import sys
from simple_live_captions.config import load_config
from simple_live_captions.gui.main_window import SimpleLiveCaptionsApp

def setup_logging(config):
    """Setup logging configuration"""
    if config.get("enable_logging", True):
        logging.basicConfig(
            level=logging.INFO,
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('simple_live_captions.log', encoding='utf-8')
            ],
            force=True
        )
    else:
        logging.disable(logging.CRITICAL)

def main():
    """Main application entry point"""
    try:
        logging.basicConfig(level=logging.INFO)
        config = load_config()
        setup_logging(config)
        logging.info("Starting Simple Live Captions application")

        app = SimpleLiveCaptionsApp(config)
        app.mainloop()

    except Exception as e:
        logging.error(f"Application error: {e}")
        print(f"An error occurred: {e}")
        sys.exit(1)

    finally:
        logging.info("Simple Live Captions application ended")

if __name__ == "__main__":
    main()
