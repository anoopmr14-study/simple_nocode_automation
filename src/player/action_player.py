"""
Action Player
--------------
Reads recorded automation file and executes actions.
"""

import time
import pyautogui
from pynput import keyboard
from src.report.execution_tracker import ExecutionTracker
from src.core.action import Action
from src.player.smart_click import SmartClickExecutor


pyautogui.FAILSAFE = True


class ActionPlayer:

    def __init__(self, actions):
        self.actions = actions
        self.speed = 1.0   # 1 = normal, 2 = 2x faster, 0.5 = slower
        self.running = False
        self.stop_listener = None
        self.smart_click = SmartClickExecutor()
        self.tracker = ExecutionTracker()

    def start_stop_listener(self):
        """Start hotkey listener to stop automation"""
        self.stop_listener = keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+q': self.stop_execution
        })

        self.stop_listener.start()

    def stop_execution(self):
        print("Automation Stopped by User")
        self.running = False

    # -------------------------------------------------
    # Play File
    # -------------------------------------------------
    def play(self):
        print("Starting automation...")
         
        # Result tracker
        self.tracker.start_run()

        self.running = True
        self.start_stop_listener()

        for index, action in enumerate(self.actions):
            if not self.running:
                break

            result = self.tracker.start_step(index, action)
            try:
                print("Executing:", action)
                self.execute_action(action)

                result.mark_success()

            except Exception as e:
                result.mark_failed(str(e))

                # Stop execution on failure (configurable later)
                self.tracker.end_step(result)
                break

            self.tracker.end_step(result)

        self.tracker.end_run()

        return self.tracker.report

    # -------------------------------------------------
    # Execute Action
    # -------------------------------------------------
    def execute_action(self, action):
        # -----------------------------
        # Wait
        # -----------------------------
        if action.action_type in ["wait", "Wait"]:
            time.sleep(action.delay / self.speed)

        # -----------------------------
        # Mouse Move
        # -----------------------------
        elif action.action_type in ["mouse_move", "MOUSE MOVE"]:
            pyautogui.moveTo(action.x, action.y)

        # -----------------------------
        # Click Object with SmartClickExecutor (with retry and timeout)
        # -----------------------------
        elif action.action_type in ["object_click", "Click Object"]:
            self.smart_click.click_object( action)   

        elif action.action_type in ["validate_object", "Validate Object"]:
            result = self.smart_click.validate_object(action)

            if not result:
                raise Exception(f"Validation failed: {action.target}")

        # -----------------------------
        # Wait Object
        # -----------------------------
        elif action.action_type in ["wait_object", "Wait Object"]:
            self.smart_click.wait_for_object(action)

        # -----------------------------
        # Mouse Left Click
        # -----------------------------
        elif action.action_type in ["click", "Click"]:
            pyautogui.click(action.x, action.y)

        # -----------------------------
        # Mouse Right Click
        # -----------------------------
        elif action.action_type in ["right_click", "Right Click"]:
            pyautogui.rightClick(action.x, action.y)

        # -----------------------------
        # Mouse Double Click
        # -----------------------------
        elif action.action_type in ["double_click", "Double Click"]:
            pyautogui.doubleClick(action.x, action.y)

      

        # -----------------------------
        # Type Text
        # -----------------------------
        elif action.action_type in ["type", "Type"]:
            pyautogui.write(action.text)

        # -----------------------------
        # Hotkey
        # -----------------------------
        elif action.action_type in ["hotkey", "Hotkey"]:
            keys = action.text.split(" + ")
            pyautogui.hotkey(*[k.lower() for k in keys])

        # -----------------------------
        # Special Keys
        # -----------------------------
        elif action.action_type in  ["key", "Key"]:
            pyautogui.press(action.text.lower())

        else:
            print("Unknown action:", action.action_type)


# -------------------------------------------------
# Independent Test
# -------------------------------------------------
if __name__ == "__main__":

    player = ActionPlayer()

    # change to your recorded file
    player.play_file("recording.txt")