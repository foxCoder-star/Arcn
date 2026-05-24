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
    def handle(self, packet: dict) -> dict:

        source     = packet.get("source", "nlp")
        intent     = packet.get("intent")
        confidence = packet.get("confidence", 0.0)
        entities   = packet.get("entities", {})
        requires_clarification = packet.get("requires_clarification", False)

        # -------------------------
        # 1. Unknown intent
        # -------------------------
        if intent == "unknown_intent":
            return self._unknown()

        # -------------------------
        # 2. Clarification needed
        # -------------------------
        if requires_clarification:
            return self._clarify(intent, entities)

        # -------------------------
        # 3. Route to action
        # -------------------------
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