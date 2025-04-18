import subprocess
from gtts import gTTS
import asyncio
import edge_tts
import os
from typing import Optional

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

async def speak_async(text: str) -> None:
    """Asynchronously generate and play speech"""
    Speech_Output.add_message(text)
    output_file = "speech_output.mp3"
    
    try:
        # Generate speech with slower speed
        communicate = edge_tts.Communicate(
            text=text,
            voice="en-US-AriaNeural",
            rate="-10%"
        )
        await communicate.save(output_file)

        # Play the audio and wait for completion
        Speech_Output.current_process = subprocess.Popen(
            ["mpg123", output_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Wait for process to complete
        while Speech_Output.current_process.poll() is None:
            await asyncio.sleep(0.1)

    except Exception as e:
        print(f"Error in speech generation: {e}")
        raise
    finally:
        # Clean up the audio file
        if os.path.exists(output_file):
            try:
                os.remove(output_file)
            except:
                pass

def speak(text: str) -> None:
    """Synchronous interface for speech synthesis"""
    try:
        # Try to use existing event loop
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # Create new event loop if none exists
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    # Run the async function synchronously
    loop.run_until_complete(speak_async(text))
    
    # Ensure process is cleaned up
    if Speech_Output.current_process and Speech_Output.current_process.poll() is None:
        Speech_Output.current_process.terminate()