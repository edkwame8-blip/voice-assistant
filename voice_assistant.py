import speech_recognition as sr
import pyttsx3
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote_plus

WAKE_WORD = "assistant"

class VoiceAssistant:
    def __init__(self):
        # Speech Recognition
        self.recognizer = sr.Recognizer()

        # Text-to-Speech
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 180)  # Speech speed
            self.engine.setProperty("volume", 1.0)
        except Exception as e:
            print(f"Error initializing TTS: {e}")
            sys.exit(1)

        # Browser
        try:
            chrome_options = Options()
            self.driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"Error initializing Browser: {e}")
            self.driver = None

        print("Voice Assistant Started")
        self.speak("Voice assistant started.")
        self.speak(f'Say {WAKE_WORD} followed by a command.')

        # Initial noise adjustment
        print("Adjusting for ambient noise...")
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

        self.listen_loop()

    def speak(self, text):
        """Convert text to speech."""
        print("Assistant:", text)
        self.engine.say(text)
        self.engine.runAndWait()

    def process_command(self, command):
        command = command.lower().strip()

        if command.startswith("search"):
            query = command.replace("search", "", 1).strip()
            if query.startswith("for "):
                query = query.replace("for ", "", 1).strip()

            if query:
                self.speak(f"Searching for {query}")
                if self.driver:
                    url = f"https://www.google.com/search?q={quote_plus(query)}"
                    self.driver.get(url)
                else:
                    self.speak("Browser is not available.")
            else:
                self.speak("What should I search for?")

        elif "youtube" in command:
            self.speak("Opening YouTube")
            if self.driver:
                self.driver.get("https://www.youtube.com")

        elif "google" in command:
            self.speak("Opening Google")
            if self.driver:
                self.driver.get("https://www.google.com")

        elif "time" in command:
            current_time = datetime.now().strftime("%I:%M %p")
            self.speak(f"The time is {current_time}")

        elif command in ["quit", "exit", "stop", "goodbye"]:
            self.speak("Goodbye")
            if self.driver:
                self.driver.quit()
            sys.exit()

        else:
            self.speak("Sorry, I do not recognize that command.")

    def listen_loop(self):
        while True:
            try:
                with sr.Microphone() as source:
                    print("\nListening...")
                    audio = self.recognizer.listen(
                        source,
                        timeout=5,
                        phrase_time_limit=8
                    )

                text = self.recognizer.recognize_google(audio).lower()
                print("You said:", text)

                if WAKE_WORD in text:
                    command = text.split(WAKE_WORD, 1)[1].strip()

                    if command:
                        self.process_command(command)
                    else:
                        self.speak("Yes? How can I help you?")

            except sr.WaitTimeoutError:
                pass

            except sr.UnknownValueError:
                # Silent on unknown to avoid annoying spam
                pass

            except sr.RequestError:
                self.speak("Speech recognition service is unavailable.")

            except KeyboardInterrupt:
                print("\nShutting down.")
                if self.driver:
                    self.driver.quit()
                break

            except Exception as e:
                print("Error:", e)


if __name__ == "__main__":
    VoiceAssistant()



















