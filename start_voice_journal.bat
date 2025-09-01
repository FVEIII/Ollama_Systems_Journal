@echo off
cd /d "C:\Users\Frank Emmerson\Ollama_Systems_Journal"
call venv\Scripts\activate.bat
python journal_voice.py >> journal_log.txt 2>&1
