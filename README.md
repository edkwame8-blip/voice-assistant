# 🎙️ Voice Assistant

A Python-based voice assistant that listens for a wake word and controls your browser using voice commands. Built with `SpeechRecognition`, `pyttsx3`, and `Selenium`.

---

## Features

- 🔍 **Google search** by voice
- 🌐 **Open websites** — YouTube, Google
- 🕐 **Tell the time and date**
- 🔊 **Text-to-speech** responses
- 🔄 **Auto-calibrates** microphone for ambient noise
- 🌐 **Browser fallback** — works even without Chrome/Selenium

---

## Requirements

- Python 3.8+
- Google Chrome (for Selenium browser control)
- A working microphone
- Internet connection (for Google Speech Recognition)

---

## Installation

**1. Clone the repository:**
```bash
git clone https://github.com/edkwame8-blip/voice-assistant.git
cd voice-assistant
```

**2. Install dependencies:**
```bash
pip install speechrecognition pyttsx3 selenium
```

> **Windows users:** If `pyaudio` fails, install it with:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

**3. (Optional) Install ChromeDriver** for Selenium browser control:
- Download from: https://chromedriver.chromium.org/downloads
- Match the version to your installed Chrome version
- Add `chromedriver.exe` to your system PATH

---

## Usage

**Run the assistant:**
```bash
python voice_assistant.py
```

Say the wake word **"assistant"** followed by your command:

| Command | Action |
|---|---|
| `assistant search Python tutorials` | Searches Google |
| `assistant open youtube` | Opens YouTube |
| `assistant open google` | Opens Google |
| `assistant what time is it` | Tells the current time |
| `assistant what's today's date` | Tells today's date |
| `assistant help` | Lists all commands in terminal |
| `assistant quit` | Shuts down the assistant |

---

## Project Structure

```
voice-assistant/
├── voice_assistant.py   # Main assistant script
├── assistant.py         # Alternative/experimental version
├── .gitignore
└── README.md
```

---

## Troubleshooting

**Microphone not detected:**
Make sure your microphone is connected and set as the default input device in your OS settings.

**Speech recognition not working:**
Check your internet connection — the assistant uses Google's online speech recognition API.

**Chrome/Selenium errors:**
The assistant will automatically fall back to your system's default browser if Chrome or ChromeDriver is not available.

**`pyaudio` install fails on Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

---

## Author

**Edwin Mayor** — [@edkwame8-blip](https://github.com/edkwame8-blip)

---

## License

This project is open source and available under the [MIT License](LICENSE).
