"""
Simple Action Recorder
----------------------
Records mouse and keyboard actions.

Stop recording using:
CTRL + ALT + S
"""

from pynput import mouse, keyboard
from datetime import datetime


class ActionRecorder:

    def __init__(self):

        self.actions = []
        self.recording = False

        self.mouse_listener = None
        self.keyboard_listener = None
        self.hotkey_listener = None

    # -----------------------------------------------------
    # Start Recording
    # -----------------------------------------------------
    def start_recording(self):

        print("Recording Started")
        print("Press CTRL + ALT + S to stop")

        self.recording = True

        # Mouse listener
        self.mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click
        )

        # Keyboard listener
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press
        )

        # Reliable global hotkey
        self.hotkey_listener = keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+s': self.stop_recording
        })

        self.mouse_listener.start()
        self.keyboard_listener.start()
        self.hotkey_listener.start()

        self.mouse_listener.join()

    # -----------------------------------------------------
    # Mouse Move
    # -----------------------------------------------------
    def on_move(self, x, y):

        if not self.recording:
            return

        action = f"Mouse Move {x},{y}"
        self.actions.append(action)

    # -----------------------------------------------------
    # Mouse Click
    # -----------------------------------------------------
    def on_click(self, x, y, button, pressed):

        if not self.recording:
            return

        if pressed:

            if button == mouse.Button.left:
                action = "Mouse Left Click"

            elif button == mouse.Button.right:
                action = "Mouse Right Click"

            else:
                return

            self.actions.append(action)

    # -----------------------------------------------------
    # Keyboard Press
    # -----------------------------------------------------
    def on_key_press(self, key):

        if not self.recording:
            return

        try:
            char = key.char

            if char:
                action = f"Type text {char}"
                self.actions.append(action)

        except AttributeError:
            pass

    # -----------------------------------------------------
    # Stop Recording
    # -----------------------------------------------------
    def stop_recording(self):

        print("\nRecording Stopped")

        self.recording = False

        if self.mouse_listener:
            self.mouse_listener.stop()

        if self.keyboard_listener:
            self.keyboard_listener.stop()

        if self.hotkey_listener:
            self.hotkey_listener.stop()

        self.save_actions()

    # -----------------------------------------------------
    # Save File
    # -----------------------------------------------------
    def save_actions(self):

        if not self.actions:
            print("No actions recorded")
            return

        filename = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        with open(filename, "w") as f:
            for action in self.actions:
                f.write(action + "\n")

        print(f"File saved: {filename}")


# -----------------------------------------------------
# Independent Testing
# -----------------------------------------------------
if __name__ == "__main__":

    recorder = ActionRecorder()
    recorder.start_recording()