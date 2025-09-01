import pyttsx3
import whisper
import speech_recognition as sr
import os

# Initialize TTS engine
engine = pyttsx3.init()

# Load Whisper model
model = whisper.load_model("tiny")

# Temp file for saving microphone input
TEMP_FILE = os.path.join(os.getcwd(), "temp.wav")


def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()
    


def transcribe_audio():
    """Record from mic, save to WAV, and transcribe."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening... Speak now!")
        audio = recognizer.listen(source)

    # Save raw audio to disk using the proper method
    with open(TEMP_FILE, "wb") as f:
        f.write(audio.get_wav_data())

    # Confirm the file was created
    print(f"🛠 File created? {os.path.exists(TEMP_FILE)}")
    print(f"📍 Saved WAV path: {TEMP_FILE}")

    if not os.path.exists(TEMP_FILE):
        raise FileNotFoundError(f"Could not find file: {TEMP_FILE}")

    print("🧠 Transcribing...")
    result = model.transcribe(TEMP_FILE, fp16=False)
    return result["text"]


if __name__ == "__main__":
    try:
        text = transcribe_audio()
        print(f"🗣 You said: {text}")
        speak(f"You said: {text}")

        # Optional: cleanup
        if os.path.exists(TEMP_FILE):
            os.remove(TEMP_FILE)

    except Exception as e:
        print(f"❌ Error: {e}")
