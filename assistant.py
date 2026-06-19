import speech_recognition as sr
import pyttsx3
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote_plus

WAKE_WORD = "assistant"

# 🔑 Replace these with your Spotify Developer credentials
SPOTIFY_CLIENT_ID = "your_client_id"
SPOTIFY_CLIENT_SECRET = "your_client_secret"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"


class VoiceAssistant:
    def __init__(self):
        # Speech Recognition
        self.recognizer = sr.Recognizer()

        # Text-to-Speech
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 180)
        self.engine.setProperty("volume", 1.0)

        # Browser
        chrome_options = Options()
        self.driver = webdriver.Chrome(options=chrome_options)

        # Spotify
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope="user-modify-playback-state user-read-playback-state"
        ))

        print("Voice Assistant Started")
        self.speak("Voice assistant started.")
        self.speak(f"Say {WAKE_WORD} followed by a command.")

        self.listen_loop()

    def speak(self, text):
        """Convert text to speech."""
        print("Assistant:", text)
        self.engine.say(text)
        self.engine.runAndWait()

    def get_active_device(self):
        """Return the first active Spotify device ID, or None."""
        devices = self.spotify.devices()
        active = [d for d in devices["devices"] if d["is_active"]]
        if active:
            return active[0]["id"]
        elif devices["devices"]:
            return devices["devices"][0]["id"]
        return None

    def process_command(self, command):
        command = command.lower().strip()

        # --- Browser commands ---
        if command.startswith("search "):
            query = command.replace("search ", "", 1).strip()
            if query:
                self.speak(f"Searching for {query}")
                url = f"https://www.google.com/search?q={quote_plus(query)}"
                self.driver.get(url)

        elif command == "open youtube":
            self.speak("Opening YouTube")
            self.driver.get("https://www.youtube.com")

        elif command == "open google":
            self.speak("Opening Google")
            self.driver.get("https://www.google.com")

        elif command == "what time is it":
            from datetime import datetime
            current_time = datetime.now().strftime("%I:%M %p")
            self.speak(f"The time is {current_time}")

        # --- Spotify commands ---
        elif command.startswith("play "):
            song = command.replace("play ", "", 1).strip()
            self.speak(f"Playing {song} on Spotify")
            results = self.spotify.search(q=song, type="track", limit=1)
            tracks = results["tracks"]["items"]
            if tracks:
                uri = tracks[0]["uri"]
                device_id = self.get_active_device()
                self.spotify.start_playback(
                    device_id=device_id,
                    uris=[uri]
                )
            else:
                self.speak("Sorry, I couldn't find that song.")

        elif command == "pause":
            self.speak("Pausing Spotify")
            self.spotify.pause_playback()

        elif command == "resume":
            self.speak("Resuming Spotify")
            device_id = self.get_active_device()
            self.spotify.start_playback(device_id=device_id)

        elif command == "next song":
            self.speak("Skipping to next track")
            self.spotify.next_track()

        elif command == "previous song":
            self.speak("Going back to previous track")
            self.spotify.previous_track()

        elif command == "what song is this":
            current = self.spotify.current_playback()
            if current and current["is_playing"]:
                track = current["item"]["name"]
                artist = current["item"]["artists"][0]["name"]
                self.speak(f"This is {track} by {artist}")
            else:
                self.speak("Nothing is playing right now.")

        elif command.startswith("set volume "):
            level = command.replace("set volume ", "", 1).strip()
            if level.isdigit() and 0 <= int(level) <= 100:
                self.spotify.volume(int(level))
                self.speak(f"Volume set to {level}")
            else:
                self.speak("Please say a volume between 0 and 100.")

        elif command == "quit":
            self.speak("Goodbye")
            self.driver.quit()
            raise SystemExit

        else:
            self.speak("Sorry, I do not recognize that command.")

    def listen_loop(self):
        while True:
            try:
                with sr.Microphone() as source:
                    print("\nListening...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = self.recognizer.listen(
                        source, timeout=5, phrase_time_limit=10
                    )

                text = self.recognizer.recognize_google(audio).lower()
                print("You said:", text)

                if WAKE_WORD in text:
                    command = text.split(WAKE_WORD, 1)[1].strip()
                    if command:
                        self.process_command(command)

            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                self.speak("I didn't catch that.")
            except sr.RequestError:
                self.speak("Speech recognition service is unavailable.")
            except KeyboardInterrupt:
                self.speak("Shutting down.")
                self.driver.quit()
                break
            except Exception as e:
                print("Error:", e)
                self.speak("An error occurred.")


if __name__ == "__main__":
    VoiceAssistant()