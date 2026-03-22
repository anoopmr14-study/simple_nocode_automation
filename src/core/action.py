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
        w: Optional[int] = None,
        h: Optional[int] = None,                
        text: Optional[str] = None,
        delay: float = 0.0
    ):
        self.action_type = action_type  # click, type, wait, etc.
        self.target = target            # object name
        self.x = x                      # fallback x
        self.y = y                      # fallback y
        self.w = w                      # width
        self.h = h                      # height    
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
            "w": self.w,
            "h": self.h,
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
            w=data.get("w"),
            h=data.get("h"),
            text=data.get("text"),
            delay=data.get("delay", 0.0)
        )

    # -------------------------------
    # String representation (for UI)
    # -------------------------------
    def __str__(self):

        if self.action_type in ["mouse_move", "Mouse Move"]:
            return f"Mouse Move ({self.x}, {self.y})"
        
        if self.action_type in ["object_click", "Click Object"]:
            return f"Click Object  '{self.target}'  (x: {self.x}, y: {self.y}, w: {self.w}, h: {self.h})"
        
        if self.action_type in ["click", "Click"]:
            return f"Click  ({self.x}, {self.y})"

        if self.action_type in ["right_click", "Right Click"]:
            return f"Right Click  ({self.x}, {self.y})"

        if self.action_type in ["double_click", "Double Click"]:
            return f"Double Click  ({self.x}, {self.y})"

        if self.action_type in ["type", "Type"]:
            return f"Type  '{self.text}'"
        
        if self.action_type in  ["hotkey", "Hotkey"]:
            return f"Hotkey  '{self.text}'"
        
        if self.action_type in  ["key", "Key"]:
            return f"Key  '{self.text}'"

        if self.action_type in ["wait", "Wait"]:
            return f"Wait  {self.delay}s"
        
        if self.action_type in ["validate_object", "Validate Object"]:
            return f"Validate Object '{self.target}'  (x: {self.x}, y: {self.y}, w: {self.w}, h: {self.h})"

        if self.action_type in ["wait_Object", "Wait Object"]:
            return f"Wait Object '{self.target}'  (x: {self.x}, y: {self.y}, w: {self.w}, h: {self.h}) with timeout {self.delay}s"

        return self.action_type

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