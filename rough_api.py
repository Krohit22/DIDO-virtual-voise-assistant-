from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import speech_recognition as sr
from play_random_song import play_song
from plyer import notification
import pyautogui
import wikipedia
import webbrowser
from gtts import gTTS
import os
import subprocess
from genai import GenoAI
import threading

app = Flask(__name__)
CORS(app)

class SpeechOutput:
    """Class to store the spoken message"""
    def __init__(self):
        self.messages = []

    def add_message(self, message):
        """Add a message to the stored list"""
        self.messages.insert(0, message)

Speech_Output = SpeechOutput()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/get_messages')
def get_messages():
    return jsonify({'messages': Speech_Output.messages})

def speak(text):
    Speech_Output.add_message(text)
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    process = subprocess.Popen(["mpg123", "output.mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Use DEVNULL to hide output.
    process.wait()  # Wait for mpg123 to finish

def listen_for_wake_word():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word 'kiko'...")
        while True:
            audio = r.listen(source)
            try:
                content = r.recognize_google(audio, language='en-in').lower()
                if 'kiko' in content:
                    print("Wake word detected!")
                    speak("Yes? How can I help you?")
                    return True
            except Exception as e:
                print("Error recognizing wake word:", e)

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5)
            content = r.recognize_google(audio, language='en-in')
            print("You said:", content)
            return content.lower()
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None
        except Exception as e:
            print("An error occurred:", e)
            return None

def main_process():
    while True:
        if listen_for_wake_word():
            request = command()
            if not request:
                speak("Sorry, I didn't understand that. Can you please repeat?")
            elif 'play song' in request:
                speak("Playing song")
                play_song()
                jsonify({"message": "Playing song"})
            elif 'add new task' in request:
                task = request.replace("add new task", "").strip()
                if task:
                    speak("Adding task: " + task)
                    with open("./tasks.txt", "a") as file:
                        file.write(task + "\n")
            elif 'speak my tasks' in request:
                with open("./tasks.txt", "r") as file:
                    tasks = file.read()
                speak("Your tasks are: " + tasks)
            elif 'show my tasks' in request:
                with open("./tasks.txt", "r") as file:
                    tasks = file.read()
                notification.notify(
                    title="Task Reminder",
                    message=tasks,
                    app_icon=None,
                    timeout=10
                )
            elif 'open youtube' in request:
                webbrowser.open('https://www.youtube.com/')
                speak("Opening YouTube")
                Speech_Output.add_message("Opening YouTube")
                print(Speech_Output.messages)
            elif 'open' in request:
                query = request.replace("open", "").strip()
                print(f"Opening application: {query}")
                pyautogui.press('super')
                pyautogui.typewrite(query)
                pyautogui.sleep(2)
                pyautogui.press('enter')
                speak(f"Opening {query}")
            elif 'wikipedia' in request:
                speak('Searching Wikipedia...')
                query = request.replace("wikipedia", "").strip()
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia: " + results)
            elif 'on youtube' in request or 'in youtube' in request:
                query = request.replace("search", "").replace("on youtube", "").replace("in youtube", "").strip()
                webbrowser.open('https://www.youtube.com/results?search_query=' + query)
                speak("Searching on YouTube")
            elif 'on google' in request or 'in google' in request:
                query = request.replace("search", "").replace("on google", "").replace("in google", "").strip()
                webbrowser.open('https://www.google.com/search?q=' + query)
                speak("Searching on Google")
            else:
                speak("I'm sorry, I don't understand that command.")

def run_main_process():
    with app.app_context():
        main_process()

if __name__ == "__main__":
    # Check if this is the main process (not the reloader)
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug:
        background_thread = threading.Thread(target=run_main_process)
        background_thread.daemon = True
        background_thread.start()
    app.run(debug=False)