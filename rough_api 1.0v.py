from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import speech_recognition as sr
from play_random_song import play_song
from plyer import notification
import pyautogui
import wikipedia
import webbrowser
from Speak_func import speak, Speech_Output
import os
from WeatherReport import get_weather
from genai import GenoAI
import threading
import psutil
from detect_Keywords_commands import detect_command
from keywords import get_keywords_Dic
import signal


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/get_messages')
def get_messages():
    return jsonify({'messages': Speech_Output.messages})

  # Wait for mpg123 to finish

def listen_for_wake_word():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word 'Dido'...")
        while True:
            audio = r.listen(source)
            try:
                content = r.recognize_google(audio, language='en-in').lower()
                if 'dido' in content:
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
        # if listen_for_wake_word():
            keywords_Dic = get_keywords_Dic()
            request = command()
            detect_command(request)
            detected_command = detect_command(request)
            print("keywords_Dic:", keywords_Dic)  # Debugging statement
            print("Type of keywords_Dic:", type(keywords_Dic))

            if request is None: 
                print("No valid command detected, skipping...")
                continue 
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
                pyautogui.press('esc')
                pyautogui.press('super')
                pyautogui.typewrite(query)
                pyautogui.sleep(2)
                pyautogui.press('enter')
                speak(f"Opening {query}")
            elif 'close this application' in request or 'quit' in request:
                query = request.replace("close", "").replace("quit", "").strip()
                print(f"Closing application: {query}")
                pyautogui.hotkey('alt', 'f4')
                speak(f"Closing {query}")
            elif 'close tab' in request or 'close this tab' in request or 'close the tab' in request:
                pyautogui.hotkey('ctrl', 'w')
                speak("Closing tab")
            elif 'close application' in request or 'close' in request:
                    query = request.replace("close application", "").replace("close", "").strip()
                    query = query.lower().strip()
                    print(f"Attempting to close: {query}")
                    process_found = False

                    for proc in psutil.process_iter(['pid', 'name']):
                        try:
                            process_name = proc.info['name'].lower()
                            if query in process_name:  # Match process name
                                print(f"Closing process: {process_name} (PID: {proc.pid})")
                                
                                # First, try terminating gracefully
                                proc.terminate()
                                proc.wait(timeout=3)

                                # If still running, force kill
                                if proc.is_running():
                                    os.kill(proc.pid, signal.SIGTERM)  # Force close
                                    proc.kill()
                                
                                process_found = True  
                                
                        except psutil.NoSuchProcess:
                            continue  # If process disappears, move on
                        except psutil.AccessDenied:
                            speak(f"Permission denied to close {query}. Try running as administrator.")
                            continue
                    
                    if process_found:
                        speak(f"Successfully closed {query}.")  # Speak success message
                    else:
                        speak(f"Could not find an application named {query}.")  # Speak failure message
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

            elif detected_command == "weather":
                for keyword in keywords_Dic["weather"]: 
                    if keyword in request:
                        speak("Fetching weather report")
                        query = request.replace(keyword, "").strip()
                        get_weather()

                        
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