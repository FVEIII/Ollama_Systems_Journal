import pyttsx3
import whisper
import speech_recognition as sr
import os
import time
from pydub import AudioSegment
import shutil

assert shutil.which("ffmpeg"), "❌ ffmpeg is not installed or not in PATH"

# Initialize TTS engine
engine = pyttsx3.init()

# Load Whisper model (change to "tiny", "base", "small", etc.)
model = whisper.load_model("base")  # more accurate than "tiny"

# Temp file for saving mic input
TEMP_FILE = os.path.join(os.getcwd(), "temp.wav")

def speak(text):
    """Convert text to speech."""
    print(f"🗣️ You said: {text}")
    engine.say(text)
    engine.runAndWait()

def transcribe_audio():
    """Record from mic → save to WAV → normalize → transcribe."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Listening... Speak now!")
        audio = recognizer.listen(source, phrase_time_limit=5)

    # Save raw mic input
    with open(TEMP_FILE, "wb") as f:
        f.write(audio.get_wav_data())
    print(f"📁 Saved WAV path: {TEMP_FILE}")

    # Normalize volume
    audio_segment = AudioSegment.from_wav(TEMP_FILE)
    normalized_audio = audio_segment.apply_gain(+10)
    normalized_audio.export(TEMP_FILE, format="wav")

    # Optional: play back the audio input
    print("🔁 Playing back input for reference...")
    os.system(f"ffplay -nodisp -autoexit {TEMP_FILE}")

    # Transcribe
    print("🧠 Transcribing...")
    result = model.transcribe(TEMP_FILE)
    text = result["text"].strip().lower()
    print(f"🔍 Raw transcription: '{text}'")
    return text

# Main loop
while True:
    try:
        user_text = transcribe_audio()

        if not user_text.strip():
            print("⚠️ No speech detected.")
            speak("I didn’t catch that. Please try again.")
            continue

        if any(exit_word in user_text for exit_word in ["exit", "stop", "quit"]):
            speak("Goodbye!")
            break

        speak(user_text)

    except Exception as e:
        print(f"❌ Exception: {e}")
        speak("Something went wrong. Try again.")
