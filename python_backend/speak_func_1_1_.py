import whisper
import pyaudio
from TTS.api import TTS
import wave
import asyncio
import os
from playsound import playsound
import subprocess

# Global variables to store loaded models
whisper_model = None
coqui_tts = None

def load_whisper_model(model_size="medium"):
    """
    Lazy-load the Whisper model only when needed.
    """
    global whisper_model
    if whisper_model is None:
        print(f"Loading Whisper {model_size} model...")
        whisper_model = whisper.load_model(model_size)
    return whisper_model

def load_tts_model(model_name="tts_models/en/ljspeech/tacotron2-DDC"):
    """
    Lazy-load the TTS model only when needed.
    """
    global coqui_tts
    if coqui_tts is None:
        print(f"Loading TTS model: {model_name}")
        coqui_tts = TTS(model_name=model_name)
    return coqui_tts

def convert_wav(input_file, output_file):
    """
    Converts the .wav file to a clean 44.1kHz stereo format using ffmpeg.
    """
    try:
        print(f"Converting {input_file} to {output_file} using ffmpeg...")
        subprocess.run(['ffmpeg', '-i', input_file, '-ac', '2', '-ar', '44100', '-f', 'wav', output_file], check=True)
        print(f"Converted audio to: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting file: {e}")

async def transcribe_audio(audio_file, model_size="medium"):
    """
    Transcribe audio using Whisper model.
    """
    model = load_whisper_model(model_size)
    result = model.transcribe(audio_file)
    return result["text"]

async def speak(text, model_name="tts_models/en/ljspeech/tacotron2-DDC"):
    """
    Asynchronously synthesize speech from text using Coqui TTS and play it.
    """
    tts = load_tts_model(model_name)
    
    temp_audio_file = "output.wav"
    converted_audio_file = "output_converted.wav"

    try:
        print("Generating speech...")
        # Generate speech and save it to a temporary file
        tts.tts_to_file(text=text, file_path=temp_audio_file)

        if not os.path.exists(temp_audio_file):
            raise FileNotFoundError("The generated audio file does not exist.")

        # Convert the audio to a clean wav format using ffmpeg
        convert_wav(temp_audio_file, converted_audio_file)

        # Play the converted audio using playsound
        print("Playing audio...")
        playsound(converted_audio_file)

        print("Audio playback finished.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up the temporary audio files
        for file in [temp_audio_file, converted_audio_file]:
            if os.path.exists(file):
                try:
                    os.remove(file)
                except PermissionError:
                    print(f"Warning: Could not delete {file} because it is still in use.")

# If you want to run this as a standalone script for testing
async def main():
    # Only loads the TTS model, not Whisper
    for i in range(3):
        await speak(f"Hello, this is a test of the Coqui TTS model. {i}")
    
    # Uncomment to test transcription (would load Whisper model)
    # transcript = await transcribe_audio("some_audio_file.wav")
    # print(f"Transcription: {transcript}")

# Run the main coroutine
if __name__ == "__main__":
    asyncio.run(main())