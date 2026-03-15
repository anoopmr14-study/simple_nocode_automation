"""
Action Player
--------------
Reads recorded automation file and executes actions.
"""

import time
import pyautogui


class ActionPlayer:

    def __init__(self):
        pass

    # -------------------------------------------------
    # Play File
    # -------------------------------------------------
    def play_file(self, filepath):

        print(f"Playing automation file: {filepath}")

        with open(filepath, "r") as file:
            actions = file.readlines()

        for action in actions:

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
        # Wait
        # -----------------------------
        if action.startswith("Wait"):

            delay = float(action.split(" ")[1])
            time.sleep(delay)

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