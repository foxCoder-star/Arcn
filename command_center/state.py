import json
import os


STATE_FILE = "assistant_state.json"


class StateManager:

    def __init__(self):

        # Boot with default state if file doesn't exist
        if not os.path.exists(STATE_FILE):
            self._write({"listening": True})

    # -------------------------
    # Get full state
    # -------------------------
    def get_state(self) -> dict:

        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)

        except Exception:
            return {"listening": True}

    # -------------------------
    # Check if listening
    # -------------------------
    def is_listening(self) -> bool:

        return self.get_state().get("listening", True)

    # -------------------------
    # Set listening on/off
    # -------------------------
    def set_listening(self, value: bool):

        state = self.get_state()
        state["listening"] = value
        self._write(state)

    # -------------------------
    # Toggle listening
    # -------------------------
    def toggle_listening(self) -> bool:

        current = self.is_listening()
        new     = not current
        self.set_listening(new)
        return new

    # -------------------------
    # Write state to disk
    # -------------------------
    def _write(self, state: dict):

        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=4)