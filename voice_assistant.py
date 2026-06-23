import speech_recognition as sr
import pyttsx3
import sys
import webbrowser
from datetime import datetime
from urllib.parse import quote_plus

# Optional: Selenium for browser control (falls back to webbrowser if unavailable)
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

WAKE_WORD = "assistant"

# Supported commands summary (for help output)
COMMANDS = {
    "search <query>": "Search Google for a query",
    "open youtube": "Open YouTube in browser",
    "open google": "Open Google in browser",
    "what time is it": "Tells the current time",
    "what's today's date": "Tells the current date",
    "help": "Lists available commands",
    "quit / exit / stop": "Shuts down the assistant",
}


class VoiceAssistant:
    def __init__(self):
        print("=" * 40)
        print("   Voice Assistant Initializing...")
        print("=" * 40)

        self._setup_tts()
        self._setup_browser()
        self._setup_recognizer()

        print(f'\nSay "{WAKE_WORD}" followed by a command.')
        print('Say "assistant help" to list all commands.\n')
        self.speak(f"Voice assistant ready. Say {WAKE_WORD} followed by a command.")
        self.listen_loop()

    # ------------------------------------------------------------------ #
    #  Setup helpers                                                       #
    # ------------------------------------------------------------------ #

    def _setup_tts(self):
        """Initialize text-to-speech engine."""
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 175)
            self.engine.setProperty("volume", 1.0)
            print("[✓] Text-to-speech ready")
        except Exception as e:
            print(f"[✗] TTS failed to initialize: {e}")
            sys.exit(1)

    def _setup_browser(self):
        """Initialize browser (Selenium preferred, fallback to webbrowser)."""
        self.driver = None
        if SELENIUM_AVAILABLE:
            try:
                chrome_options = Options()
                chrome_options.add_argument("--start-maximized")
                # Uncomment below for headless mode (no visible window):
                # chrome_options.add_argument("--headless")
                self.driver = webdriver.Chrome(options=chrome_options)
                print("[✓] Chrome browser ready (Selenium)")
                return
            except Exception as e:
                print(f"[!] Selenium Chrome failed ({e}). Falling back to system browser.")
        # Fallback
        print("[✓] Using system default browser (webbrowser module)")

    def _setup_recognizer(self):
        """Calibrate microphone for ambient noise."""
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300          # Sensitivity
        self.recognizer.dynamic_energy_threshold = True  # Auto-adjust
        try:
            print("[~] Calibrating microphone for ambient noise...")
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1.5)
            print("[✓] Microphone ready")
        except OSError:
            print("[✗] No microphone found. Please connect a microphone and restart.")
            sys.exit(1)

    # ------------------------------------------------------------------ #
    #  Core utilities                                                      #
    # ------------------------------------------------------------------ #

    def speak(self, text: str):
        """Convert text to speech and print it."""
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def open_url(self, url: str):
        """Open a URL in Selenium or fallback browser."""
        if self.driver:
            self.driver.get(url)
        else:
            webbrowser.open(url)

    # ------------------------------------------------------------------ #
    #  Command processing                                                  #
    # ------------------------------------------------------------------ #

    def process_command(self, command: str):
        """Route a spoken command to the correct action."""
        command = command.lower().strip()

        # --- Search ---
        if command.startswith("search"):
            query = command.replace("search", "", 1).strip()
            if query.startswith("for "):
                query = query[4:].strip()
            if query:
                self.speak(f"Searching for {query}")
                self.open_url(f"https://www.google.com/search?q={quote_plus(query)}")
            else:
                self.speak("What would you like me to search for?")

        # --- Open websites ---
        elif "open youtube" in command or "youtube" in command:
            self.speak("Opening YouTube")
            self.open_url("https://www.youtube.com")

        elif "open google" in command:
            self.speak("Opening Google")
            self.open_url("https://www.google.com")

        # --- Time & Date ---
        elif "time" in command:
            current_time = datetime.now().strftime("%I:%M %p")
            self.speak(f"The time is {current_time}")

        elif "date" in command or "today" in command:
            today = datetime.now().strftime("%A, %B %d, %Y")
            self.speak(f"Today is {today}")

        # --- Help ---
        elif command == "help":
            self.speak("Here are the commands I support:")
            for cmd, description in COMMANDS.items():
                print(f"  • {cmd}: {description}")
            self.speak("I've printed the full list in the terminal.")

        # --- Quit ---
        elif command in {"quit", "exit", "stop", "goodbye", "bye"}:
            self.speak("Goodbye! Shutting down.")
            if self.driver:
                self.driver.quit()
            sys.exit(0)

        # --- Unknown ---
        else:
            self.speak(f"Sorry, I didn't understand '{command}'. Say 'assistant help' for a list of commands.")

    # ------------------------------------------------------------------ #
    #  Main listening loop                                                 #
    # ------------------------------------------------------------------ #

    def listen_loop(self):
        """Continuously listen for the wake word then process commands."""
        while True:
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    audio = self.recognizer.listen(
                        source,
                        timeout=6,
                        phrase_time_limit=10
                    )

                text = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {text}")

                if WAKE_WORD in text:
                    command = text.split(WAKE_WORD, 1)[1].strip()
                    if command:
                        self.process_command(command)
                    else:
                        self.speak("Yes? How can I help you?")

            except sr.WaitTimeoutError:
                # No speech detected — keep looping silently
                pass
            except sr.UnknownValueError:
                # Could not understand audio — keep looping silently
                pass
            except sr.RequestError as e:
                self.speak("Could not connect to speech recognition service. Check your internet.")
                print(f"[!] Speech recognition error: {e}")
            except KeyboardInterrupt:
                print("\n[!] Interrupted by user. Shutting down.")
                if self.driver:
                    self.driver.quit()
                sys.exit(0)
            except Exception as e:
                print(f"[!] Unexpected error: {e}")


# ------------------------------------------------------------------ #
#  Entry point                                                         #
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    VoiceAssistant()
