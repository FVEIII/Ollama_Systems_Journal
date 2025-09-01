import pyttsx3
import whisper
import speech_recognition as sr
import os
import time
from datetime import datetime
from pydub import AudioSegment
import subprocess
import shutil

# Constants
MODEL_NAME = "llama3"
JOURNAL_PATH = "coffee_sim/coffee_sim.md"
TEMP_FILE = os.path.join(os.getcwd(), "temp.wav")

# Check ffmpeg
assert shutil.which("ffmpeg"), "❌ ffmpeg is not installed or not in PATH"

# Create journal file if missing
if not os.path.exists(JOURNAL_PATH):
    os.makedirs(os.path.dirname(JOURNAL_PATH), exist_ok=True)
    with open(JOURNAL_PATH, "w", encoding="utf-8") as f:
        f.write("# ☕ Coffee Simulation Journal\n\n")

# Initialize TTS engine
engine = pyttsx3.init()

# Optional: Set voice (index 1 is often Zira on Windows)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change index as needed
engine.setProperty('rate', 180)  # Optional speed tweak

# Load Whisper model
model = whisper.load_model("base")

def speak(text):
    print(f"🧠 Speaking: {text}")
    engine.say(text)
    engine.runAndWait()

def transcribe_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening... Speak now!")
        audio = recognizer.listen(source, phrase_time_limit=5)

    with open(TEMP_FILE, "wb") as f:
        f.write(audio.get_wav_data())
    print(f"📁 Audio saved: {TEMP_FILE}")

    # Normalize volume
    audio_segment = AudioSegment.from_wav(TEMP_FILE)
    normalized_audio = audio_segment.apply_gain(+5)  # Lower gain
    normalized_audio.export(TEMP_FILE, format="wav")

    # Transcribe
    print("🧠 Transcribing...")
    result = model.transcribe(TEMP_FILE)
    text = result["text"].strip().lower()
    print(f"🔍 Transcription: '{text}'")
    return text

def query_ollama(prompt, model=MODEL_NAME):
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            encoding="utf-8",  # 🔧 Force proper decoding
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Ollama Error: {e}")
        return "Sorry, I had trouble thinking that through."


def log_to_journal(prompt, response):
    timestamp = datetime.now().strftime("%Y-%m-%d – %I:%M %p")
    entry = f"""
## 🗓️ {timestamp}

🎙 **Prompt:** {prompt}

🤖 **Response:** {response}

---
"""
    with open(JOURNAL_PATH, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"📝 Logged to journal: {JOURNAL_PATH}")

# Main loop
while True:
    try:
        user_text = transcribe_audio()

        if not user_text.strip():
            speak("I didn’t catch that. Please try again.")
            continue

        if any(exit_word in user_text for exit_word in ["exit", "stop", "quit"]):
            speak("Goodbye!")
            break

        response = query_ollama(user_text)
        speak(response)
        log_to_journal(user_text, response)

    except Exception as e:
        print(f"❌ Exception: {e}")
        speak("Something went wrong. Try again.")
