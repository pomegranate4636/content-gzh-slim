"""P1 state graph with the two human gates preserved and non-skippable."""

from __future__ import annotations


class InvalidTransition(ValueError):
    """Raised when a transition skips a required state or leaves a terminal state."""


class StateMachine:
    WAITING_STATES = frozenset({"waiting_direction", "waiting_final"})
    TERMINAL_STATES = frozenset({"distribution_optional", "abandoned", "blocked"})
    GATE_TRANSITIONS = {
        ("waiting_direction", "direction_approved"),
        ("waiting_final", "final_approved"),
    }
    _FORWARD = {
        "created": "direction_working",
        "direction_working": "waiting_direction",
        "waiting_direction": "direction_approved",
        "direction_approved": "context_ready",
        "context_ready": "draft_working",
        "draft_working": "waiting_final",
        "waiting_final": "final_approved",
        "final_approved": "saving",
        "saving": "saved",
        "saved": "distribution_optional",
    }

    @classmethod
    def next_states(cls, current: str) -> frozenset[str]:
        if current in cls.TERMINAL_STATES:
            return frozenset()
        if current not in cls._FORWARD:
            raise InvalidTransition(f"unknown state: {current}")
        return frozenset({cls._FORWARD[current], "abandoned", "blocked"})

    @classmethod
    def require_transition(cls, current: str, target: str) -> None:
        if target not in cls.next_states(current):
            raise InvalidTransition(f"illegal transition: {current} -> {target}")
        if (current, target) in cls.GATE_TRANSITIONS:
            raise InvalidTransition(
                f"gate transition requires explicit human approval: {current} -> {target}"
            )

    @classmethod
    def require_gate_approval(cls, current: str, target: str) -> None:
        if (current, target) not in cls.GATE_TRANSITIONS:
            raise InvalidTransition(f"not a gate approval transition: {current} -> {target}")
