import speech_recognition as sr
from play_random_song import play_song
from plyer import notification
import pyautogui
import wikipedia
import webbrowser
from gtts import gTTS
import os
import pygame
import time
import subprocess
import whisper
import pyaudio
from TTS.api import TTS
import wave
import asyncio  # For asynchronous programming

# Load the Whisper model
whisper_model = whisper.load_model("medium")  # Use "tiny", "base", "small", "medium", or "large"

# Load the Coqui TTS model
coqui_tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")  # Default English model

async def speak(text):
    """
    Asynchronously synthesize speech from text using Coqui TTS and play it.

    Args:
        text (str): The text to be spoken.
    """
    try:
        print("Generating speech...")
        # Generate speech and save it to a temporary file
        temp_audio_file = "output.wav"
        coqui_tts.tts_to_file(text=text, file_path=temp_audio_file)

        # Initialize pygame mixer
        pygame.mixer.init()

        # Load the generated audio file
        print("Playing audio...")
        pygame.mixer.music.load(temp_audio_file)

        # Play the audio
        pygame.mixer.music.play()

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)  # Sleep for a short duration

        # Stop the mixer and release the file
        pygame.mixer.music.stop()
        pygame.mixer.quit()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up the temporary audio file
        if os.path.exists(temp_audio_file):
            try:
                os.remove(temp_audio_file)
            except PermissionError:
                print("Warning: Could not delete the audio file because it is still in use.")

async def listen_for_wake_word():
    """
    Asynchronously listen for the wake word "Dido".
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word 'Dido'...")
        while True:
            audio = r.listen(source)
            try:
                content = r.recognize_google(audio, language='en-in').lower()
                if 'dido' in content:
                    print("Wake word detected!")
                    await speak("Yes? How can I help you?")
                    return True
            except Exception as e:
                print("Error recognizing wake word:", e)

async def command():
    """
    Asynchronously record audio from the microphone and transcribe it using Whisper.

    Returns:
        str: Transcribed text (or None if an error occurs).
    """
    # Audio configuration
    FORMAT = pyaudio.paInt16  # 16-bit audio format
    CHANNELS = 1  # Mono audio
    RATE = 16000  # Sample rate (16 kHz)
    CHUNK = 1024  # Buffer size
    RECORD_SECONDS = 5  # Duration of the recording

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Start recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Say something!")
    frames = []

    # Record audio in chunks
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio as a WAV file
    output_wav_filename = "temp_audio.wav"
    with wave.open(output_wav_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    # Transcribe the audio using Whisper
    try:
        print("Transcribing audio...")
        result = whisper_model.transcribe(output_wav_filename, language="en")
        content = result["text"].strip().lower()
        print("You said:", content)
        return content
    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        return None
    finally:
        # Clean up the temporary WAV file
        if os.path.exists(output_wav_filename):
            os.remove(output_wav_filename)

async def main_process():
    """
    Asynchronously handle the main process.
    """
    while True:
        request = await command()
        if not request:
            await speak("Sorry, I didn't understand that. Can you please repeat?")
        elif 'play song' in request:
            await speak("Playing song")
            play_song()
        elif 'add new task' in request:
            task = request.replace("add new task", "").strip()
            if task:
                await speak("Adding task: " + task)
                with open("./tasks.txt", "a") as file:
                    file.write(task + "\n")
        elif 'speak my tasks' in request:
            with open("./tasks.txt", "r") as file:
                tasks = file.read()
            await speak("Your tasks are: " + tasks)
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
            await speak("Opening YouTube")
        elif 'open' in request:
            query = request.replace("open", "").strip()
            print(f"Opening application: {query}")
            pyautogui.press('super')
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press('enter')
            await speak(f"Opening {query}")
        elif 'wikipedia' in request:
            await speak('Searching Wikipedia...')
            query = request.replace("wikipedia", "").strip()
            results = wikipedia.summary(query, sentences=2)
            await speak("According to Wikipedia: " + results)
        elif 'on youtube' in request or 'in youtube' in request:
            query = request.replace("search", "").replace("on youtube", "").replace("in youtube", "").strip()
            webbrowser.open('https://www.youtube.com/results?search_query=' + query)
            await speak("Searching on YouTube")
        elif 'on google' in request or 'in google' in request:
            query = request.replace("search", "").replace("on google", "").replace("in google", "").strip()
            webbrowser.open('https://www.google.com/search?q=' + query)
            await speak("Searching on Google")
        else:
            await speak("I'm sorry, I don't understand that command.")

# Run the main process asynchronously
async def main():
    await main_process()

# Start the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())