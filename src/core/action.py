# src/core/action.py

from typing import Optional, Dict


class Action:
    """
    Represents a single automation step.
    Example:
        Click object
        Click coordinate
        Type text
        Wait
    """

    def __init__(
        self,
        action_type: str,
        target: Optional[str] = None,
        x: Optional[int] = None,
        y: Optional[int] = None,
        text: Optional[str] = None,
        delay: float = 0.0
    ):
        self.action_type = action_type  # click, type, wait, etc.
        self.target = target            # object name
        self.x = x                      # fallback x
        self.y = y                      # fallback y
        self.text = text                # for typing
        self.delay = delay              # wait before action

    # -------------------------------
    # Convert to dictionary (for JSON)
    # -------------------------------
    def to_dict(self) -> Dict:
        return {
            "action_type": self.action_type,
            "target": self.target,
            "x": self.x,
            "y": self.y,
            "text": self.text,
            "delay": self.delay
        }

    # -------------------------------
    # Create object from dictionary
    # -------------------------------
    @staticmethod
    def from_dict(data: Dict):
        return Action(
            action_type=data.get("action_type"),
            target=data.get("target"),
            x=data.get("x"),
            y=data.get("y"),
            text=data.get("text"),
            delay=data.get("delay", 0.0)
        )

    # -------------------------------
    # String representation (for UI)
    # -------------------------------
    def __str__(self):
        if self.action_type == "click":
            if self.target:
                return f"Click [{self.target}] (fallback: {self.x},{self.y})"
            return f"Click ({self.x},{self.y})"

        elif self.action_type == "type":
            return f"Type '{self.text}'"

        elif self.action_type == "wait":
            return f"Wait {self.delay}s"

        return f"{self.action_type}"
    

# -------------------------------
# Independent Test
# -------------------------------
if __name__ == "__main__":
    action = Action(
        action_type="click",
        target="edit",
        x=100,
        y=200
    )

    print("Action Object:", action)

    data = action.to_dict()
    print("Serialized:", data)

    new_action = Action.from_dict(data)
    print("Deserialized:", new_action)