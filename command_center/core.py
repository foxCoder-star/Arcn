from router import Router
from state import StateManager


class CommandCenter:

    def __init__(self, tools: dict):

        # Router handles intent → action mapping
        self.router = Router(tools)

        # State manages system-level state
        self.state = StateManager()

    # -------------------------
    # Main entry point
    # Receives packet from NLP
    # or Vision module
    # -------------------------
    # Intents that should ALWAYS take priority
PRIORITY_INTENTS = {
    "stop_cancel", "greet", "how_are_you",
    "tell_time", "tell_date", "cancel_timer"
}

def handle(self, packet: dict) -> dict:

    source     = packet.get("source", "nlp")
    intent     = packet.get("intent")
    entities   = packet.get("entities", {})
    requires_clarification = packet.get("requires_clarification", False)

    # Priority intents always route directly
    if intent in PRIORITY_INTENTS:
        self.state.set_last_intent(intent)
        return self.router.route(intent, entities, source)

    # If unknown or clarification but last was ask_question
    if intent == "unknown_intent" or requires_clarification:
        last = self.state.get_last_intent()
        if last == "ask_question":
            intent = "ask_question"
            requires_clarification = False
        elif intent == "unknown_intent":
            return self._unknown()
        else:
            return self._clarify(intent, entities)

    self.state.set_last_intent(intent)
    return self.router.route(intent, entities, source)
    # -------------------------
    # Clarification response
    # -------------------------
    def _clarify(self, intent: str, entities: dict) -> dict:

        return self._response(
            status       = "clarifying",
            intent       = intent,
            response     = "I'm not quite sure what you mean — could you say that again?",
            action_taken = False
        )

    # -------------------------
    # Unknown intent response
    # -------------------------
    def _unknown(self) -> dict:

        return self._response(
            status       = "unknown",
            intent       = "unknown_intent",
            response     = "I didn't catch that — could you repeat it?",
            action_taken = False
        )

    # -------------------------
    # Standard response packet
    # -------------------------
    def _response(
        self,
        status      : str,
        intent      : str,
        response    : str,
        action_taken: bool
    ) -> dict:

        return {
            "status"      : status,
            "intent"      : intent,
            "response"    : response,
            "action_taken": action_taken
        }