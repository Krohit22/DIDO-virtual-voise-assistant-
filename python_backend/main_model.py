import re
import time
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import speech_recognition as sr
from brightness_up_and_down import change_brightness
from play_random_song import play_song
from plyer import notification
import pyautogui
import wikipedia
import webbrowser
from Speak_func import speak, Speech_Output
import os
from WeatherReport import get_weather
import threading
import psutil
from detect_Keywords_commands import detect_command
from keywords import get_keywords_Dic
import signal
from bluetooth_features import bluetooth_on_and_off, is_bluetooth_on
from volume_up_and_down import change_volume , current_volume
from Battery_status import get_battery_status, is_plugged_in


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
                content = r.recognize_google(audio, language='en-US').lower()
                if 'hello dido' in content:
                    print("Wake word detected!")
                    speak("Yes, How can I help you?")
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
            print("You said:", content.lower())
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
    time.sleep(0.5)
    get_battery_status()
    speak("I am listening")

    while True:
        # if listen_for_wake_word():
            keywords_Dic = get_keywords_Dic()
            request = command()
            detect_command(request)
            detected_command = detect_command(request)
            print(detected_command)


            if request is None: 
                print("No valid command detected, skipping...")
                continue 
            elif detected_command == "play_song":
                for keyword in keywords_Dic["play_song"]: 
                    if keyword in request:
                        speak("Playing song")
                        play_song()
                        jsonify({"message": "Playing song"})
            elif detected_command == "tasks":
                for keyword in keywords_Dic["tasks"]: 
                    if keyword in request:
                        task = request.replace("add new task", "").strip()
                        if task:
                            speak("Adding task: " + task)
                            with open("./tasks.txt", "a") as file:
                                file.write(task + "\n")
            elif detected_command == "speak_tasks":
                for keyword in keywords_Dic["speak_tasks"]: 
                    if keyword in request:
                        with open("./tasks.txt", "r") as file:
                            tasks = file.read()
                        speak("Your tasks are: " + tasks)
            elif detected_command == "show_tasks":
                for keyword in keywords_Dic["show_tasks"]: 
                    if keyword in request:
                        try:
                            with open("tasks.txt", "r") as file:  # Make sure to open the file
                                tasks = file.read()
                                if not tasks.strip():  # Check if file is empty or only whitespace
                                    print("There are no tasks on the list.")
                                else:
                                    notification.notify(
                                        title="Task Reminder",
                                        message=tasks,
                                        app_icon=None,
                                        timeout=10
                                    )
                        except FileNotFoundError:
                            print("Task file not found.")

            elif detected_command == "open_youtube":
                for keyword in keywords_Dic["open_youtube"]: 
                    if keyword in request:
                        speak("Opening YouTube")
                        webbrowser.open('https://www.youtube.com/')
                        Speech_Output.add_message("Opening YouTube")
                        print(Speech_Output.messages)
            elif detected_command == "open_application":
    # Get all possible opening keywords
                open_keywords = keywords_Dic["open_application"]
                
                # Find which keyword was actually used in the request
                used_keyword = next((kw for kw in open_keywords if kw in request), None)
                
                if used_keyword:
                    # Extract JUST the application name by removing ONLY the first occurrence of the keyword
                    app_name = request.replace(used_keyword, "", 1).strip()
                    
                    if app_name:
                        # Standardize app name (remove extra "launcher" if present)
                        app_name = re.sub(r'\s*(launcher|app|application|program|software)\s*', '', app_name, flags=re.IGNORECASE)
                        
                        # Try direct execution first for known apps
                        KNOWN_APPS = {
                            'epic games': r'C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe',
                            'spotify': 'spotify.exe',
                            'chrome': 'chrome.exe'
                            # Add more apps here
                        }
                        
                        # Fuzzy matching for known apps
                        matched_app = None
                        for known_app in KNOWN_APPS:
                            if known_app in app_name.lower():
                                matched_app = known_app
                                break
                        
                        if matched_app:
                            try:
                                os.startfile(KNOWN_APPS[matched_app])
                                speak(f"Opening {matched_app}")
                                continue
                            except:
                                pass  # Fall back to search method
                        
                        # Search method
                        try:
                            pyautogui.press('esc')
                            time.sleep(0.3)
                            pyautogui.press('super')
                            time.sleep(1)
                            pyautogui.typewrite(app_name)
                            time.sleep(2)
                            pyautogui.press('enter')
                            speak(f"Opening {app_name}")
                        except Exception as e:
                            speak("Sorry, I had trouble opening that application")
                            print(f"Error: {e}")
            elif 'close this application' in request or 'quit current application' in request or 'close this app' in request or 'quit current app' in request or 'close that application' in request or 'quit active application' in request  or 'quit current app' in request or 'close that app' in request or 'quit active app' in request:
                query = request.replace("close", "").replace("quit", "").strip()
                print(f"Closing application: {query}")
                pyautogui.hotkey('alt', 'f4')
                speak(f"Closing {query}")
            elif detected_command == "close_tab":
                close_tab = False
                for keyword in keywords_Dic["close_tab"]: 
                    if keyword in request and not close_tab:
                        speak("Closing tab")
                        time.sleep(1)
                        pyautogui.hotkey('ctrl', 'w')
                        close_tab = True

            elif detected_command == "close_application":
                for keyword in keywords_Dic["close_application"]: 
                    if keyword in request:
                        query = request.replace(keyword, "").strip()
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
            elif detected_command == "wikipedia":
                matched_keyword = next(
                    (keyword for keyword in keywords_Dic["wikipedia"] if keyword in request), None
                )

                if matched_keyword:
                    speak('Searching Wikipedia...')
                    query = request.replace(matched_keyword, "").replace("search", "").replace("about", "").strip()
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia: " + results)

            elif detected_command == "search_youtube":
                for keyword in keywords_Dic["search_youtube"]: 
                    if keyword in request:
                        query = request.replace("search", "").replace(keyword, "").strip()
                        webbrowser.open('https://www.youtube.com/results?search_query=' + query)
                        speak("Searching on YouTube")
            elif detected_command == "search_google":
                for keyword in keywords_Dic["search_google"]: 
                    if keyword in request:
                        query = request.replace("search", "").replace(keyword,"").strip()
                        webbrowser.open('https://www.google.com/search?q=' + query)
                        speak("Searching on Google")

            elif detected_command == "weather":
                for keyword in keywords_Dic["weather"]: 
                    if keyword in request:
                        speak("Fetching weather report")
                        query = request.replace(keyword, "").strip()
                        get_weather()
            elif detected_command == "bluetooth_on":
                for keyword in keywords_Dic["bluetooth_on"]: 
                    if keyword in request:
                        query = request.replace(keyword,"").strip()
                        speak(f"Searching for {query} on Bluetooth")
                        if is_bluetooth_on():
                            speak("Bluetooth is already on.")
                        else:
                            speak("Turning on Bluetooth.")
                            time.sleep(1)
                            bluetooth_on_and_off()                
            elif detected_command == "bluetooth_off":
                for keyword in keywords_Dic["bluetooth_off"]: 
                    if keyword in request:
                        query = request.replace(keyword,"").strip()
                        speak(f"Turning off Bluetooth")
                        if is_bluetooth_on():
                            speak("Turning off Bluetooth.")
                            bluetooth_on_and_off()
                        else:
                            speak("Bluetooth is already off.")
            elif detected_command == "volume_up":
                for keyword in keywords_Dic["volume_up"]: 
                    if keyword in request:
                        query = request.replace(keyword,"").replace("%","").replace("to","").replace("by","").strip()              
                        speak(f"Volume increased by {query} percent")
                        print(f"Volume increased by {query} percent")
                        if query == "":
                            change_volume(4)
                        else:
                            change_volume(int(query))
            elif detected_command == "volume_down":
                for keyword in keywords_Dic["volume_down"]: 
                    if keyword in request:
                        query = request.replace(keyword,"").replace("%","").replace("to","").replace("by","").strip()
                        speak(f"Volume decreased by {query} percent")
                        print(f"Volume decreased by {query} percent")
                        if query == "":
                                change_volume(-4)
                        else:
                                change_volume(-int(query))
            elif detected_command == "mute":
                for keyword in keywords_Dic["mute"]: 
                    if keyword in request:
                        query = request.replace(keyword,"").strip()
                        speak(f"Muting volume")
                        print(f"Muting volume")
                        curr_volume = current_volume()
                        change_volume(0)
            elif detected_command == "unmute":
                for keyword in keywords_Dic["unmute"]: 
                    if keyword in request:
                        query = request.replace(keyword,"").strip()
                        speak(f"unmuted volume")
                        print(f"unmuted volume")
                        change_volume(curr_volume)
            elif detected_command == "current_volume":
                for keyword in keywords_Dic["current_volume"]: 
                    if keyword in request:
                        query = request.replace(keyword,"").strip()
                        speak(f"Current volume is {current_volume()} percent")
                        print(f"Current volume is {current_volume()} percent")  
            elif detected_command == "battery_status":
                for keyword in keywords_Dic["battery_status"]: 
                    if keyword in request:
                        query = request.replace(keyword,"").strip()
                        get_battery_status()
            elif detected_command == "brightness_up":
                for keyword in keywords_Dic["brightness_up"]: 
                    if keyword in request:
                        query = request.replace(keyword, "").replace("%", "").replace("to", "").replace("by", "").strip()
                        speak(f"Brightness increased by {query} percent")
                        print(f"Brightness increased by {query} percent")
                        if query == "":
                            change_brightness(4)
                        else:
                            change_brightness(int(query))
            elif detected_command == "brightness_down":
                for keyword in keywords_Dic["brightness_down"]: 
                    if keyword in request:
                        query = request.replace(keyword,"").replace("%","").replace("to","").replace("by","").strip()
                        speak(f"Brightness decreased by {query} percent")
                        print(f"Brightness decreased by {query} percent")
                        if query == "":
                            change_brightness(4)
                        else:
                            change_brightness(-int(query))
            elif psutil.sensors_battery().power_plugged and psutil.sensors_battery().percent == 100:
                 get_battery_status()
            elif psutil.sensors_battery().power_plugged and psutil.sensors_battery().percent < 15:
                 get_battery_status()
            else:
                speak("I'm sorry, I don't understand that command.")

def run_main_process():
    with app.app_context():        main_process()

if __name__ == "__main__":
    # Check if this is the main process (not the reloader)
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug:
        background_thread = threading.Thread(target=run_main_process)
        background_thread.daemon = True
        background_thread.start()
    app.run(debug=False)   