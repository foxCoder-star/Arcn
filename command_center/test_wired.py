import sys
import os

sys.path.append(os.path.abspath("../nlp"))
sys.path.append(os.path.abspath("../tools_assistant"))
sys.path.append(os.path.abspath("../speech"))

os.chdir(os.path.abspath("../nlp"))

from pipeline import NLPBrain
from core import CommandCenter
from registry import TOOLS
from speaker import speak
from listener import listen

# Boot
nlp = NLPBrain()
cc  = CommandCenter(TOOLS)

speak("Arcn online.")

# Live loop
while True:

    text = listen()

    if not text:
        continue

    if "goodbye" in text or "shut down" in text:
        speak("Shutting down.")
        break

    # NLP processes
    packet = nlp.predict(text)
    packet["source"] = "nlp"

    # CC handles
    result = cc.handle(packet)

    # Speak the response
    response = result.get("response", "")
    if response:
        speak(response)