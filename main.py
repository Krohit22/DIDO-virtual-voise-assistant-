from flask import Flask, Request, jsonify

import pyttsx3
import speech_recognition as sr
from play_random_song import play_song
from plyer import notification
import pyautogui
import wikipedia
import webbrowser

app = Flask(__name__)

engine = pyttsx3.init()
voices = engine.getProperty('voices')     #getting details of current voice
engine.setProperty('rate', 116)     #setting up new voice rate
engine.setProperty('voice', voices[2].id)   #changing index, changes voices. 0 for

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
            print("you said.....")
            print("Command : " + content)
        except Exception as e:
            print("please say again....")
    return content

def main_process():
   
    while True:
        request = command().lower()

        if 'hello' in request:
            speak("Hello, How can I help you?")
        elif 'play song' in request:
             speak("playing song")
             play_song()
        elif 'add new task' in request:
            task = request.replace("add new task", "")
            task = task.strip()
            if task != "":
                speak("adding task: " + task)
                with open("./tasks.txt", "a") as file:
                    file.write(task + "\n")
        elif 'speak my tas' in request:
            speak("your tasks are")
            with open("./tasks.txt", "r") as file:
                speak("work we have to do today is : "+file.read())
        elif 'show my task' in request: 
             with open("./tasks.txt", "r") as file:
                 task = file.read()
             notification.notify(
                 title = "Task Reminder",
                 message = task,
                 app_icon = None,
                 timeout = 10
             )
        elif 'open youtube' in request:
            webbrowser.open('https://www.youtube.com/')
        elif 'open' in request: 
            query = request.replace("open", "")
            pyautogui.press('super')
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press('enter')
        elif 'wikipedia' in request:
            speak('searching wikipedia...')
            query = request.replace("wikipedia", "")
            query = request.replace("search on wikipedia ", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)

        elif 'on youtube' in request or 'in youtube' in request:
             query = request.replace("search", "")
             query = query.replace("on youtube", "")
             query = query.replace("in youtube", "")
             query = query.strip()
             webbrowser.open('https://www.youtube.com/results?search_query='+query) 
             
        elif 'on google' in request or 'in google' in request:
             query = request.replace("search", "")
             query = query.replace("on google", "")
             query = query.replace("in google", "")
             query = query.strip()
             webbrowser.open('https://www.google.com/search?q='+query) 


main_process()