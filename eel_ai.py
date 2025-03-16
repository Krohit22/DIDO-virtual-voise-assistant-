import eel
import pyttsx3
import speech_recognition as sr
from play_random_song import play_song
from plyer import notification
import pyautogui
import wikipedia
import webbrowser
import os

# Initialize Eel
eel.init("web")  # Folder containing your frontend files

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')  # Getting details of current voice
engine.setProperty('rate', 116)  # Setting up new voice rate
engine.setProperty('voice', voices[2].id)  # Changing index, changes voices

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def command():
    content = " "
    while content == " ":
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        try:
            content = r.recognize_google(audio, language='en-in')
            print("You said:", content)
        except Exception as e:
            print("Please say again....")
    return content

# Expose Python functions to the frontend
@eel.expose
def process_command():
    request = command().lower()

    if 'hello' in request:
        speak("Hello, How can I help you?")
        return "Hello, How can I help you?"
    elif 'play song' in request:
        speak("playing song")
        play_song()
        return "Playing song"
    elif 'add new task' in request:
        task = request.replace("add new task", "").strip()
        if task:
            speak(f"adding task: {task}")
            with open("tasks.txt", "a") as file:
                file.write(task + "\n")
            return f"Added task: {task}"
        else:
            return "No task provided"
    elif 'speak my task' in request:
        try:
            with open("tasks.txt", "r") as file:
                tasks = file.read()
            speak("your tasks are")
            speak("work we have to do today is : " + tasks)
            return tasks
        except FileNotFoundError:
            return "No tasks found"
    elif 'show my task' in request:
        try:
            with open("tasks.txt", "r") as file:
                tasks = file.read()
            notification.notify(
                title="Task Reminder",
                message=tasks,
                app_icon=None,
                timeout=10
            )
            return tasks
        except FileNotFoundError:
            return "No tasks found"
    elif 'open youtube' in request:
        webbrowser.open('https://www.youtube.com/')
        return "Opened YouTube"
    elif 'open' in request:
        query = request.replace("open", "").strip()
        if query:
            pyautogui.press('super')
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press('enter')
            speak(f"Opened {query}")
            return f"Opened {query}"
        else:
            return "No query provided"
    elif 'wikipedia' in request:
        query = request.replace("wikipedia", "").replace("search on wikipedia", "").strip()
        if query:
            speak('searching wikipedia...')
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to wikipedia")
                speak(results)
                return results
            except wikipedia.exceptions.DisambiguationError:
                return "Multiple results found. Please refine your query."
            except wikipedia.exceptions.PageError:
                return "No results found on Wikipedia."
            except Exception as e:
                return f"Error searching Wikipedia: {str(e)}"
        else:
            return "No query provided"
    elif 'on youtube' in request or 'in youtube' in request:
        query = request.replace("search", "").replace("on youtube", "").replace("in youtube", "").strip()
        if query:
            webbrowser.open(f'https://www.youtube.com/results?search_query={query}')
            return f"Searching YouTube for: {query}"
        else:
            return "No query provided"
    elif 'on google' in request or 'in google' in request:
        query = request.replace("search", "").replace("on google", "").replace("in google", "").strip()
        if query:
            webbrowser.open(f'https://www.google.com/search?q={query}')
            return f"Searching Google for: {query}"
        else:
            return "No query provided"
    else:
        return "Command not recognized"

# Start the Eel application
eel.start("./eel.html", size=(800, 600))