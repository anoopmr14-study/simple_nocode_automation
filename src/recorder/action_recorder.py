"""
Simple Action Recorder
----------------------
Records mouse and keyboard actions.

Stop recording using:
CTRL + ALT + S
"""

import json
import time
from pynput import mouse, keyboard
from datetime import datetime
from src.core.action import Action


class ActionRecorder:

    def __init__(self, callback=None, stop_callback=None):
        self.record_callback = callback
        self.stop_callback = stop_callback

        self.actions = []  # fallback (for testing)
        self.recording = False

        self.mouse_listener = None
        self.keyboard_listener = None
        self.hotkey_listener = None

        # For delay recording
        self.last_event_time = time.time()

        # For mouse noise removal
        self.last_mouse_position = None

        # For double click detection
        self.last_click_time = 0
        self.double_click_threshold = 0.4

        # Track pressed modifier keys
        self.ctrl_pressed = False
        self.alt_pressed = False
        self.shift_pressed = False

    # -----------------------------------------------------
    # Start Recording
    # -----------------------------------------------------
    def start_recording(self):

        print("Recording Started. CTRL + ALT + S to stop")

        self.recording = True

        # Mouse listener
        self.mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click
        )

        # Keyboard listener
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
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
    # Emit action to callback or store in list
    # -----------------------------------------------------
    def _emit(self, action):
        if self.record_callback:
            self.record_callback(action)
        else:
            self.actions.append(action)  # fallback for testing

    # -----------------------------------------------------
    # Record Delay between actions 
    # -----------------------------------------------------
    def record_delay(self):
        """Record wait time between actions"""

        current_time = time.time()
        delay = round(current_time - self.last_event_time, 2)

        if delay > 0.2:  # ignore very small delays
            action = Action(action_type="wait", delay=delay)
            self._emit(action)
            #self.actions.append(f"Wait {delay}")

        self.last_event_time = current_time

    # -----------------------------------------------------
    # Mouse Move
    # -----------------------------------------------------
    def on_move(self, x, y):
        if self.recording:
            # store only last position
             self.last_mouse_position = (x, y)
        
        
    # -----------------------------------------------------
    # Mouse Click
    # -----------------------------------------------------
    def on_click(self, x, y, button, pressed):
        if not self.recording:
            return

        print(f"on_click at {(x, y)} with {button} {'Pressed' if pressed else 'Released'}")

        if pressed:

            self.record_delay()

            # record final mouse position before click
            if self.last_mouse_position:
                mx, my = self.last_mouse_position
                self._emit(Action(action_type="mouse_move", x=mx, y=my))
                # self.actions.append(f"Mouse Move {mx},{my}")
            else:
                mx, my = x, y

            current_time = time.time()

            # Detect double click
            if current_time - self.last_click_time < self.double_click_threshold:
                #self.actions.append("Mouse Double Click")
                action = Action(action_type="double_click", x=mx, y=my)
            else:
                if button == mouse.Button.left:
                    #self.actions.append("Mouse Left Click")
                    action = Action(action_type="click", x=mx, y=my)

                elif button == mouse.Button.right:
                    #self.actions.append("Mouse Right Click")
                    action = Action(action_type="right_click", x=mx, y=my)

            self._emit(action)
            self.last_click_time = current_time

    # -----------------------------------------------------
    # Keyboard Press
    # -----------------------------------------------------
    def on_key_press(self, key):
        """
        Detect typing and dynamic hotkeys
        Examples recorded:
        Type text H
        Hotkey Ctrl + C
        Hotkey Ctrl + Shift + S
        """
        print(f"on_key_press {key}")    

        if not self.recording:
            return
        
        try:
            # character key
            char = key.char

            if char:

                # record delay between actions
                self.record_delay()

                # Fix control character issue (Ctrl + A -> Ctrl + Z)
                if self.ctrl_pressed and ord(char) < 32:
                    char = chr(ord(char) + 96)

                # Build modifier list
                modifiers = []

                if self.ctrl_pressed:
                    modifiers.append("Ctrl")

                if self.alt_pressed:
                    modifiers.append("Alt")

                if self.shift_pressed:
                    modifiers.append("Shift")

                if modifiers:
                    hotkey = " + ".join(modifiers + [char.upper()])
                    self._emit(Action(action_type="hotkey", text=hotkey))
                    # self.actions.append(f"Hotkey {hotkey}")
                else:
                    # Regular character typing
                    self._emit(Action(action_type="type", text=char))
                    # self.actions.append(f"Type text {char}")               

        except AttributeError:
            # handle special keys
            if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
                self.ctrl_pressed = True

            elif key in (keyboard.Key.alt_l, keyboard.Key.alt_r):
                self.alt_pressed = True

            elif key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r):
                self.shift_pressed = True

            # Record special hotkeys like Alt+Tab
            self.record_delay()

            if key == keyboard.Key.tab and self.alt_pressed:
                self._emit(Action(action_type="hotkey", text="Alt + Tab"))
                # self.actions.append("Hotkey Alt + Tab")

            elif key == keyboard.Key.enter:
                self._emit(Action(action_type="key", text="Enter"))
                # self.actions.append("Key Enter")

            elif key == keyboard.Key.backspace:
                self._emit(Action(action_type="key", text="Backspace"))
                # self.actions.append("Key Backspace")

    # -----------------------------------------------------
    # Keyboard Release
    # -----------------------------------------------------
    def on_key_release(self, key):

        if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            print(f"Reset ctrl") 
            self.ctrl_pressed = False

        elif key in (keyboard.Key.alt_l, keyboard.Key.alt_r):
            print(f"Reset atl") 
            self.alt_pressed = False

        elif key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r):
            print(f"Reset shift")
            self.shift_pressed = False


    # -----------------------------------------------------
    # Stop Recording
    # -----------------------------------------------------
    def stop_recording(self):
        print("\nRecording Stopped")
        
        # Set recording flag to False to stop listeners from adding more actions
        self.recording = False

        # Save actions to file
        #self.save_actions()

        # Stop listeners
        if self.mouse_listener:
            self.mouse_listener.stop()

        if self.keyboard_listener:
            self.keyboard_listener.stop()

        if self.hotkey_listener:
            self.hotkey_listener.stop()

        # ✅ notify UI
        if self.stop_callback:
            self.stop_callback()

    # -----------------------------------------------------
    # Save File
    # -----------------------------------------------------
    def save_actions(self):
        print("save_actions " + str(self.actions))

        if not self.actions:
            print("No actions recorded")
            return

        filename = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        data = [action.to_dict() for action in self.actions]    

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        # with open(filename, "w") as f:
        #     for action in self.actions:
        #         print("action " + str(action)) 
        #         f.write(str(action) + "\n")

        #     # force write to disk
        #     f.flush()                

        print("File saved: " + str(filename))


# -----------------------------------------------------
# Independent Testing
# -----------------------------------------------------
if __name__ == "__main__":

    recorder = ActionRecorder()
    recorder.start_recording()