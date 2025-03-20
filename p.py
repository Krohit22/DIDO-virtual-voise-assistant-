import whisper  # OpenAI Whisper for speech-to-text
import pyaudio  # For recording audio from the microphone
import wave  # For saving recorded audio as a WAV file
from TTS.api import TTS  # Coqui TTS for text-to-speech
import os

# Load the Whisper model
print("Loading Whisper model...")
whisper_model = whisper.load_model("base")  # Use "tiny", "base", "small", "medium", or "large"

# Load the Coqui TTS model
print("Loading Coqui TTS model...")
coqui_tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")  # Default English model

def record_audio(output_wav_filename, record_seconds=5):
    """
    Record audio from the microphone and save it as a WAV file.

    Args:
        output_wav_filename (str): Path to save the recorded audio.
        record_seconds (int): Duration of the recording in seconds.
    """
    # Audio configuration
    FORMAT = pyaudio.paInt16  # 16-bit audio format
    CHANNELS = 1  # Mono audio
    RATE = 16000  # Sample rate (16 kHz)
    CHUNK = 1024  # Buffer size

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Start recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Recording...")
    frames = []

    # Record audio in chunks
    for _ in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio as a WAV file
    with wave.open(output_wav_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

def transcribe_audio(wav_filename):
    """
    Transcribe audio from a WAV file using Whisper.

    Args:
        wav_filename (str): Path to the WAV file.

    Returns:
        str: Transcribed text.
    """
    print("Transcribing audio...")
    result = whisper_model.transcribe(wav_filename, language="en")
    return result["text"].strip()

def speak_text(text):
    """
    Speak text using Coqui TTS.

    Args:
        text (str): Text to be spoken.
    """
    print("Speaking text...")
    # Generate speech and save it to a temporary file
    temp_audio_file = "temp_output.wav"
    coqui_tts.tts_to_file(text=text, file_path=temp_audio_file)

    # Play the generated audio using a system command
    os.system(f"mpg123 {temp_audio_file}")  # Requires mpg123 to be installed

    # Clean up the temporary audio file
    os.remove(temp_audio_file)

def main():
    # Record audio from the microphone
    output_wav_filename = "recorded_audio.wav"
    record_audio(output_wav_filename, record_seconds=5)

    # Transcribe the recorded audio
    transcribed_text = transcribe_audio(output_wav_filename)
    print(f"You said: {transcribed_text}")

    # Speak the transcribed text
    if transcribed_text:
        speak_text(transcribed_text)
    else:
        print("No text was transcribed.")

    # Clean up the recorded audio file
    os.remove(output_wav_filename)

if __name__ == "__main__":
    main()