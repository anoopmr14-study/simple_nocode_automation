"""
Action Player
--------------
Reads recorded automation file and executes actions.
"""

import time
import pyautogui
from pynput import keyboard
from src.player.smart_click import SmartClickExecutor


pyautogui.FAILSAFE = True


class ActionPlayer:

    def __init__(self):
        self.speed = 1.0   # 1 = normal, 2 = 2x faster, 0.5 = slower
        self.running = False
        self.stop_listener = None
        self.smart_click = SmartClickExecutor()

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
    def play_file(self, filepath):
        print(f"Playing automation file: {filepath}")

        # Set running flag and start hotkey listener
        self.running = True
        self.start_stop_listener()

        # Read actions from file
        with open(filepath, "r") as file:
            actions = file.readlines()

        # Execute actions sequentially
        for action in actions:
            if not self.running:
                break

            action = action.strip()
            if not action:
                continue

            print("Executing:", action)
            self.execute_action(action)

    # -------------------------------------------------
    # Execute Action
    # -------------------------------------------------
    def execute_action(self, action):

        # -----------------------------
        # Click Object with SmartClickExecutor (with retry and timeout)
        # -----------------------------
        if action.startswith("Click Object"):
            object_name = action.replace("Click Object ", "")

            # Using SmartClickExecutor for object clicks
            self.smart_click.click_object(object_name, None, None, 200, 0.75)

        # -----------------------------
        # Wait
        # -----------------------------
        if action.startswith("Wait"):

            delay = float(action.split(" ")[1])
            #time.sleep(delay)
            time.sleep(delay / self.speed)

        # -----------------------------
        # Mouse Move
        # -----------------------------
        elif action.startswith("Mouse Move"):

            pos = action.replace("Mouse Move ", "")
            x, y = pos.split(",")

            pyautogui.moveTo(int(x), int(y))

        # -----------------------------
        # Mouse Left Click
        # -----------------------------
        elif action == "Mouse Left Click":

            pyautogui.click()

        # -----------------------------
        # Mouse Right Click
        # -----------------------------
        elif action == "Mouse Right Click":

            pyautogui.rightClick()

        # -----------------------------
        # Mouse Double Click
        # -----------------------------
        elif action == "Mouse Double Click":

            pyautogui.doubleClick()

        # -----------------------------
        # Type Text
        # -----------------------------
        elif action.startswith("Type text"):

            text = action.replace("Type text ", "")
            pyautogui.write(text)

        # -----------------------------
        # Hotkey
        # -----------------------------
        elif action.startswith("Hotkey"):

            keys = action.replace("Hotkey ", "").split(" + ")

            pyautogui.hotkey(*[k.lower() for k in keys])

        # -----------------------------
        # Special Keys
        # -----------------------------
        elif action.startswith("Key"):

            key = action.replace("Key ", "").lower()

            pyautogui.press(key)

        else:
            print("Unknown action:", action)


# -------------------------------------------------
# Independent Test
# -------------------------------------------------
if __name__ == "__main__":

    player = ActionPlayer()

    # change to your recorded file
    player.play_file("recording.txt")