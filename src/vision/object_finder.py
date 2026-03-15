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

from src.object_repo.object_manager import ObjectRepositoryManager


class ObjectFinder:

    def __init__(self, confidence=0.8):

        # minimum match confidence
        self.confidence = confidence

        self.repo = ObjectRepositoryManager()

    # -------------------------------------------------
    # Capture current screen
    # -------------------------------------------------
    def capture_screen(self):

        with mss.mss() as sct:
            monitor = sct.monitors[1]  # primary monitor
            img = sct.grab(monitor)

        screen = np.array(img)

        # convert BGRA -> BGR
        screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)

        return screen

    # -------------------------------------------------
    # Find object on screen
    # -------------------------------------------------
    def find_object(self, object_name):

        obj = self.repo.get_object(object_name)

        if not obj:
            print(f"Object not found in repository: {object_name}")
            return None

        template = cv2.imread(obj["image"])

        if template is None:
            print("Failed to load template image")
            return None

        screen = self.capture_screen()

        result = cv2.matchTemplate(
            screen,
            template,
            cv2.TM_CCOEFF_NORMED
        )

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val < self.confidence:
            return None

        h, w = template.shape[:2]

        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2

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