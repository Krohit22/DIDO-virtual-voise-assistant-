from flask import Flask, jsonify
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


app = Flask(__name__)
CORS(app)

# def speak(text):
#     tts = gTTS(text=text, lang='en')
#     tts.save("output.mp3")  # Save audio to a file
#     os.system("mpg123 output.mp3")  # Play the audio using mpg321
#     os.remove("output.mp3")



def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    process = subprocess.Popen(["mpg123", "output.mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) #use DEVNULL to hide output.
    process.wait()  # Wait for mpg123 to finish
    

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

@app.route('/main_process', methods=['POST'])
def main_process():
    request = command()
    if not request:
        return jsonify({"message": "Sorry, I didn't understand that."})

    if 'hello' in request:
        speak("Hello, How can I help you?")
        return jsonify({"message": "Hello, How can I help you?"})
    elif 'play song' in request:
        speak("Playing song")
        play_song()
        return jsonify({"message": "Playing song"})
    elif 'add new task' in request:
        task = request.replace("add new task", "").strip()
        if task:
            speak("Adding task: " + task)
            with open("./tasks.txt", "a") as file:
                file.write(task + "\n")
            return jsonify({"message": "Adding task: " + task})
    elif 'speak my tasks' in request:
        with open("./tasks.txt", "r") as file:
            tasks = file.read()
        speak("Your tasks are: " + tasks)
        return jsonify({"message": "Your tasks are: " + tasks})
    elif 'show my tasks' in request:
        with open("./tasks.txt", "r") as file:
            tasks = file.read()
        notification.notify(
            title="Task Reminder",
            message=tasks,
            app_icon=None,
            timeout=10
        )
        return jsonify({"message": "Task Reminder: " + tasks})
    elif 'open youtube' in request:
        webbrowser.open('https://www.youtube.com/')
        speak("Opening YouTube")
        return jsonify({"message": "Opening YouTube"})
    elif 'open' in request:
        query = request.replace("open", "").strip()
        print(f"Opening application: {query}")
        pyautogui.press('super')
        pyautogui.typewrite(query)
        pyautogui.sleep(2)
        pyautogui.press('enter')
        speak(f"Opening {query}")
        return jsonify({"message": f"Opening {query}"})
    elif 'wikipedia' in request:
        speak('Searching Wikipedia...')
        query = request.replace("wikipedia", "").strip()
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia: " + results)
        return jsonify({"message": results})
    elif 'on youtube' in request or 'in youtube' in request:
        query = request.replace("search", "").replace("on youtube", "").replace("in youtube", "").strip()
        webbrowser.open('https://www.youtube.com/results?search_query=' + query)
        speak("Searching on YouTube")
        return jsonify({"message": "Searching on YouTube"})
        
    elif 'on google' in request or 'in google' in request:
        query = request.replace("search", "").replace("on google", "").replace("in google", "").strip()
        webbrowser.open('https://www.google.com/search?q=' + query)
        speak("Searching on Google")
        return jsonify({"message": "Searching on Google"})
    else:
        speak("Sorry, I didn't understand that command.")
        return jsonify({"message": "Sorry, I didn't understand that command."})

if __name__ == "__main__":
    app.run(debug=True)