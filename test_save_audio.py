import os
import speech_recognition as sr

TEMP_FILE = os.path.join(os.getcwd(), "temp.wav")

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("🎤 Speak now...")
    audio = recognizer.listen(source)

with open(TEMP_FILE, "wb") as f:
    f.write(audio.get_wav_data())

print(f"✅ File written? {os.path.exists(TEMP_FILE)}")
print(f"📍 File path: {TEMP_FILE}")
