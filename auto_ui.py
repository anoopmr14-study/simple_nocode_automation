import os
import sys
import time
import threading
import re

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton
from PySide6.QtCore import Qt

import pyautogui
import pytesseract
import mss
import cv2
import numpy as np
from pynput import keyboard


# -------------------------
# Import and configure pytesseract
# -------------------------
try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False

# Configure portable Tesseract if available
def _configure_tesseract():
    """
    Configure pytesseract to use portable Tesseract bundled with the app.
    
    Supports both:
    - Frozen executable (PyInstaller bundle)
    - Development mode (running from source)
    
    Expects tesseract/ directory at SmartAutomation root with:
    - tesseract.exe (binary)
    - tessdata/ (language data)
    """
    if not PYTESSERACT_AVAILABLE:
        return
    
    try:
        # Determine base path: executable if frozen, script directory otherwise
        if getattr(sys, 'frozen', False):
            # Running from PyInstaller bundle
            base_path = os.path.dirname(sys.executable)
            print("Running from PyInstaller bundle " + str(base_path))
        else:
            # base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))    # Inside src
            base_path = os.path.dirname(os.path.abspath(__file__)) # outside src
            print("Running outside PyInstaller bundle " + str(base_path))
       
        
        tesseract_exe = os.path.join(base_path, "tesseract", "tesseract.exe")
        tessdata_path = os.path.join(base_path, "tesseract", "tessdata")

        print(tessdata_path)
        
        # Only configure if portable Tesseract exists
        if os.path.exists(tesseract_exe) and os.path.exists(tessdata_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_exe
            os.environ["TESSDATA_PREFIX"] = tessdata_path
        else:
            print(f"[OCR] Local tesseract not found, pytesseract will use system PATH")
    except Exception as e:
        print(f"[OCR] Warning: Could not configure portable Tesseract: {e}")

# Initialize portable Tesseract on import
_configure_tesseract()


STOP_FLAG = False


class SimpleAutomation(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple OCR Automation")
        self.setGeometry(200, 200, 500, 400)

        # Layout
        layout = QVBoxLayout()

        # Command Text Editor
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Type commands like:\nClick on File\nType Hello\nClick on Save")
        layout.addWidget(self.editor)

        # Create Insert Screenshot Object button
        self.insert_btn = QPushButton("Insert Screenshot Object")
        self.insert_btn.clicked.connect(self.insert_object)
        layout.addWidget(self.insert_btn)

        # Create Play Button
        self.play_btn = QPushButton("Play")
        self.play_btn.clicked.connect(self.start_execution)
        layout.addWidget(self.play_btn)

        # Set the layout
        self.setLayout(layout)

        # Listen the hotkey in the background
        self.start_hotkey_listener()

    # -------------------------
    # Global Stop Hotkey
    # -------------------------
    def start_hotkey_listener(self):
        def on_activate():
            global STOP_FLAG
            STOP_FLAG = True
            print("STOP triggered")

        self.listener = keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+s': on_activate
        })
        self.listener.start()

    # -------------------------
    # Insert Screenshot Object Button
    # -------------------------
    def insert_object(self):
        from object_capture import ObjectCapture

        self.hide()

        # Keep reference so Qt doesn't destroy the window
        self.capture_tool = ObjectCapture(self)

        self.capture_tool.start_capture()


    # -------------------------
    # Play Button
    # -------------------------
    def start_execution(self):
        global STOP_FLAG
        STOP_FLAG = False

        commands = self.editor.toPlainText().splitlines()

        self.showMinimized()
        time.sleep(1)

        thread = threading.Thread(target=self.execute_commands, args=(commands,))
        thread.start()

    # -------------------------
    # OCR + Execute
    # -------------------------
    def execute_commands(self, commands):
        global STOP_FLAG

        for command in commands:
            if STOP_FLAG:
                break

            command = command.strip()
            cmd = command.lower()

            # -----------------
            # CLICK ON TEXT
            # -----------------
            if cmd.startswith("click on"):
                text = command[8:].strip()
                self.click_text(text)

            # -----------------
            # TYPE TEXT
            # -----------------
            elif cmd.startswith("type"):
                text = command[4:].strip()
                pyautogui.write(text, interval=0.05)

            # -----------------
            # HOTKEY
            # Example: Hotkey Ctrl+X
            # -----------------
            elif cmd.startswith("hotkey"):
                combo = command[6:].strip()
                self.execute_hotkey(combo)

            # -----------------
            # MOUSE MOVE
            # Example: Mouse Move 500,300
            # -----------------
            elif cmd.startswith("mouse move"):
                coords = command[10:].strip()
                try:
                    x, y = coords.split(",")
                    pyautogui.moveTo(int(x), int(y), duration=0.2)
                except:
                    print("Invalid Mouse Move format")

            # -----------------
            # MOUSE LEFT CLICK
            # -----------------
            elif cmd.startswith("mouse left click"):
                pyautogui.click()

            # -----------------
            # MOUSE RIGHT CLICK
            # -----------------
            elif cmd.startswith("mouse right click"):
                pyautogui.rightClick()

            # -----------------
            # MOUSE DOUBLE CLICK
            # -----------------
            elif cmd.startswith("mouse double click"):
                pyautogui.doubleClick()

            else:
                print(f"Unknown command: {command}")

            time.sleep(0.5)

        print("Execution finished")

    # -------------------------
    # Execute Hotkey
    # -------------------------
    def execute_hotkey(self, combo):

        try:
            keys = combo.replace(" ", "").lower().split("+")
            pyautogui.hotkey(*keys)
        except Exception as e:
            print(f"Hotkey error: {e}")

    # -------------------------
    # Screenshot + OCR
    # -------------------------
    def get_screen_text_positions(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)

        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        results = []

        # data Dictionary format
        # data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        # print(data)
        # for i in range(len(data['text'])):
        #     if int(data['conf'][i]) > 60:
        #         text = data['text'][i]
        #         x = data['left'][i]
        #         y = data['top'][i]
        #         w = data['width'][i]
        #         h = data['height'][i]
        #         results.append((text, x, y, w, h))

        # Extract OCR data as DataFrame
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DATAFRAME)
        print(data)

        # Clean Unwanted Data
        data = data[data.text.notna()]
        data = data[data.text.str.strip() != ""]
        data = data[data.conf.astype(float) > 0]

        # Print Each Row with Coordinates
        for index, row in data.iterrows():
            if int(row['conf']) > 60:
                text = row['text']
                x = int(row['left'])
                y = int(row['top'])
                w = int(row['width'])
                h = int(row['height'])
                results.append((text, x, y, w, h))


        return results

    # -------------------------
    # Click Based on OCR Text
    # -------------------------
    def click_text(self, target):
        positions = self.get_screen_text_positions()
        print(positions)

        for text, x, y, w, h in positions:
            if target.lower() in text.lower():
                center_x = x + w // 2
                center_y = y + h // 2
                pyautogui.moveTo(center_x, center_y, duration=0.3)
                pyautogui.click()
                return

        print(f"Text '{target}' not found")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleAutomation()
    window.show()
    sys.exit(app.exec())