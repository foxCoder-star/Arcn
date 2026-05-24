import sys
import os

# Point to NLP and tools modules
sys.path.append(os.path.abspath("../nlp"))
sys.path.append(os.path.abspath("../tools_assistant"))

# Set working directory to nlp so model paths resolve correctly
os.chdir(os.path.abspath("../nlp"))

from pipeline import NLPBrain
from core import CommandCenter
from registry import TOOLS

# Boot both modules
nlp = NLPBrain()
cc  = CommandCenter(TOOLS)

# Live loop
while True:
    text = input("\nYou: ")
    if text.lower() == "quit":
        break

    # NLP processes text
    packet = nlp.predict(text)
    packet["source"] = "nlp"

    print(f"NLP: {packet}")

    # CC handles packet
    result = cc.handle(packet)
    print(f"CC:  {result}")