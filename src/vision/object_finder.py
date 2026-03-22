"""
Object Finder Engine

This module finds UI objects on the screen using image matching.

Uses:
- OpenCV for template matching
- MSS for fast screenshot capture

Returns the center coordinates of detected object.
"""

import cv2
import numpy as np
import mss
from PIL import Image

from PySide6.QtCore import QRect
from PySide6.QtGui import QGuiApplication
from pyscreeze import screenshot

from src.object_repo.object_manager import ObjectRepositoryManager


class ObjectFinder:

    def __init__(self, confidence=0.5):

        # minimum match confidence
        self.confidence = confidence

        self.repo = ObjectRepositoryManager()

    # -------------------------------------------------
    # Capture current screen
    # -------------------------------------------------
    def capture_screen(self, rect=None):
        print(f"Object_finder::capture_screen() - Capturing screen with rect: {rect}")
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # primary monitor
            if rect is not None:
                monitor = rect

            print(f"Object_finder::capture_screen() - Capturing screen with monitor settings: {monitor}")
            img = sct.grab(monitor)
        
        img = Image.frombytes("RGB", img.size, img.rgb)
        screen = np.array(img)

        # convert RGB -> BGR
        # screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
        screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
        # screen = screen[:, :, :3]  # ensure 3 channels

        # Sample for debugging
        image_path = f"results//finder_sample.png"
        Image.fromarray(screen).save(image_path)

        return screen

    # -------------------------------------------------
    # Find object on screen
    # -------------------------------------------------
    def find_object(self, object_name, confidence=None):

        obj = self.repo.get_object(object_name)
        print(f"Object_finder::find_object() - Looking for object: {object_name} in repository {obj}" )

        if not obj:
            print(f"Object_finder::find_object() - Object not found in repository: {object_name}")
            return None

        template = cv2.imread(obj["image"])

        if template is None:
            print(f"Object_finder::find_object() - Failed to load template image for object: {object_name} at path: {obj['image']}")
            return None

        # Capture current screen
        # FIXME:: Capture only specific region for better performance
        rect = None
        if None not in (obj["x"], obj["y"], obj["w"], obj["h"]):

            screen = QGuiApplication.primaryScreen()
            dpr = screen.devicePixelRatio()

            rect = {
                "left": int(obj["x"] * dpr),
                "top": int(obj["y"] * dpr),
                "width": int(obj["w"] * dpr),
                "height": int(obj["h"] * dpr),
}

        current_screen = self.capture_screen(rect=rect)
        print(f"Object_finder::find_object() - Screenshot taken for object {object_name} \
                rect: {rect}  current screen shape: {current_screen.shape}")

        # ✅ Convert to grayscale (IMPORTANT)
        current_screen_gray = cv2.cvtColor(current_screen, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # Perform template matching (image comparison)
        result = cv2.matchTemplate(
            current_screen_gray,
            template_gray,
            cv2.TM_CCOEFF_NORMED
        )

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        used_confidence = confidence if confidence else self.confidence

        print(f"Object_finder::find_object() - Match confidence: {max_val}")

        if max_val < used_confidence:
            return None

        h, w = template.shape[:2]

        # center_x = max_loc[0] + w // 2
        # center_y = max_loc[1] + h // 2
        center_x = rect["left"] + rect["width"] // 2 if rect else max_loc[0] + w // 2
        center_y = rect["top"] + rect["height"] // 2 if rect else max_loc[1] + h // 2   

        print(f"Object_finder::find_object() - center X : {center_x}  center Y: {center_y}")
 
        return (center_x, center_y)

    # -------------------------------------------------
    # Wait until object appears
    # -------------------------------------------------
    def wait_for_object(self, name, timeout=10):

        import time

        start = time.time()

        while time.time() - start < timeout:

            loc = self.find_object(name)

            if loc:
                return loc

            time.sleep(0.5)

        return None


# -----------------------------------------------------
# Independent Test
# -----------------------------------------------------

if __name__ == "__main__":

    finder = ObjectFinder()

    location = finder.find_object("FileMenu")

    if location:
        print("Object found at:", location)
    else:
        print("Object not found")