import subprocess
from gtts import gTTS
import subprocess
import asyncio
import edge_tts


class SpeechOutput:
    """Class to store the spoken message"""
    def __init__(self):
        self.messages = []

    def add_message(self, message):
        """Add a message to the stored list"""
        self.messages.insert(0, message)

Speech_Output = SpeechOutput()

# def speak(text):
#     Speech_Output.add_message(text)
#     tts = gTTS(text=text, lang='en')
#     tts.save("output.mp3")
#     process = subprocess.Popen(["mpg123", "output.mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Use DEVNULL to hide output.
#     process.wait()  # Wait for mpg123 to finish


# Use edge-tts to generate speech asynchronously

async def speak_async(text):
    Speech_Output.add_message(text)
    output_file = "output.mp3"

    # Use SSML to slow down the speech (adjust rate value as needed)
    

    # Use edge-tts to generate speech with slower speed
    communicate = edge_tts.Communicate(text, voice="en-US-AriaNeural", rate="-10%")
    await communicate.save(output_file)

    # Play the generated speech
    process = subprocess.Popen(["mpg123", output_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    process.wait()

def speak(text):
    asyncio.run(speak_async(text))

