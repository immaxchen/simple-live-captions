# Simple Live Captions

A simple Python app for live captioning system audio using offline models.

Developed for the poor souls who aren't able to upgrade to Windows 11 🙋‍♂️

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/immaxchen/simple-live-captions.git
   cd simple-live-captions
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Download the models

   * Create a `models/` directory if it doesn't exist.
   * Download speech recognition models from the [VOSK models page](https://alphacephei.com/vosk/models).
   * Unzip the downloaded models into the `models/` directory.

   Example:

   ```bash
   mkdir models
   wget https://alphacephei.com/vosk/models/vosk-model-ja-0.22.zip
   unzip vosk-model-ja-0.22.zip -d models/
   ```

## Usage

1. Edit `config.json` to configure the settings. (optional)

2. Run the live captions app with:

   ```bash
   python -m simple_live_captions
   ```

