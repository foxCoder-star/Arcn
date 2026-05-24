import os
import asyncio
import time
import edge_tts


# -------------------------
# Config
# -------------------------
VOICE = "en-US-ChristopherNeural"
AUDIO_FILE = "voice.mp3"


# -------------------------
# Async TTS core
# -------------------------
async def _speak_async(text: str):

    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(AUDIO_FILE)
    os.system(f"afplay {AUDIO_FILE}")
    time.sleep(0.3)
    os.remove(AUDIO_FILE)


# -------------------------
# Public speak function
# -------------------------
def speak(text: str):

    if not text or not text.strip():
        return

    print(f"Arcn: {text}")
    asyncio.run(_speak_async(text))