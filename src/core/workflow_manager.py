# src/core/workflow_manager.py

import os, json
from datetime import datetime
from typing import List
from src.core.action import Action


class WorkflowManager:
    """
    Manages automation workflow (list of actions)
    """

    def __init__(self, root_folder="results/workflows"):
        self.default_root_folder = root_folder
        self.actions: List[Action] = []

    # -------------------------------
    # Add action
    # -------------------------------
    def add_action(self, action: Action):
        self.actions.append(action)

    # -------------------------------
    # Delete action
    # -------------------------------
    def delete_action(self, index: int):
        if 0 <= index < len(self.actions):
            del self.actions[index]

    # -------------------------------
    # Move action up
    # -------------------------------
    def move_up(self, index: int):
        if index > 0:
            self.actions[index - 1], self.actions[index] = \
                self.actions[index], self.actions[index - 1]

    # -------------------------------
    # Move action down
    # -------------------------------
    def move_down(self, index: int):
        if index < len(self.actions) - 1:
            self.actions[index + 1], self.actions[index] = \
                self.actions[index], self.actions[index + 1]

    # -------------------------------
    # Get all actions
    # -------------------------------
    def get_actions(self) -> List[Action]:
        return self.actions

    # -------------------------------
    # Save workflow
    # -------------------------------
    def save(self, file_path=None):
        # generate filename in root folder if not provided
        if not file_path:
            os.makedirs(self.default_root_folder, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"workflow_{timestamp}.json"
            file_path = os.path.join(self.default_root_folder, file_name)

        # ensure .json
        if not file_path.endswith(".json"):
            file_path += ".json"

        data = [a.to_dict() for a in self.actions]

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        print("Saved:", file_path)
        return file_path

    # -------------------------------
    # Load workflow
    # -------------------------------
    def load(self, file_path=None):
        if not os.path.exists(file_path):
            return

        # FIXME:: Load from most recent file in default folder if file_path is None
        if file_path is None:
            # Implementation for loading most recent file from default folder can be added here
            pass

        with open(file_path, "r") as f:
            data = json.load(f)

        self.actions = [Action.from_dict(d) for d in data]

    # -------------------------------
    # Clear workflow
    # -------------------------------
    def clear(self):
        self.actions = []

    # -------------------------------
    # Debug print
    # -------------------------------
    def print_workflow(self):
        print("\n--- Workflow ---")
        for i, action in enumerate(self.actions):
            print(f"{i}: {action}")
        print("----------------\n")


# -------------------------------
# Independent Test
# -------------------------------
if __name__ == "__main__":
    wm = WorkflowManager()

    wm.add_action(Action("click", target="edit", x=100, y=200))
    wm.add_action(Action("type", text="Hello World"))
    wm.add_action(Action("wait", delay=2))

    wm.print_workflow()

    wm.move_up(2)
    wm.print_workflow()

    # Save
    file_path = wm.save("test_workflow.json")

    # Reload
    wm2 = WorkflowManager()
    wm2.load(file_path)
    wm2.print_workflow()