import sys
import os

sys.path.append(os.path.abspath("../tools_assistant"))

from registry import TOOLS
from core import CommandCenter

# Boot CC with real tools
cc = CommandCenter(TOOLS)

# Test 1 — real tool execution (open youtube)
print("\n--- Test 1: Open YouTube ---")
packet = {
    "source"                : "nlp",
    "intent"                : "open_youtube",
    "confidence"            : 0.95,
    "entities"              : {},
    "requires_clarification": False
}
print(cc.handle(packet))

# Test 2 — clarification
print("\n--- Test 2: Clarification ---")
packet = {
    "source"                : "nlp",
    "intent"                : "open_youtube",
    "confidence"            : 0.62,
    "entities"              : {},
    "requires_clarification": True
}
print(cc.handle(packet))

# Test 3 — unknown intent
print("\n--- Test 3: Unknown intent ---")
packet = {
    "source"                : "nlp",
    "intent"                : "unknown_intent",
    "confidence"            : 0.30,
    "entities"              : {},
    "requires_clarification": False
}
print(cc.handle(packet))

# Test 4 — no tool registered
print("\n--- Test 4: No tool registered ---")
packet = {
    "source"                : "nlp",
    "intent"                : "send_message",
    "confidence"            : 0.91,
    "entities"              : {"person": "mom"},
    "requires_clarification": False
}
print(cc.handle(packet))