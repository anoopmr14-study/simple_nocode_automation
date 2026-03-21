"""
Smart Object Click Engine

Provides reliable clicking on UI objects using:
- image detection
- retry mechanism
- timeout handling
- coordinate fallback
"""

import time
import pyautogui

from src.vision.object_finder import ObjectFinder


class SmartClickExecutor:

    def __init__(self):

        self.finder = ObjectFinder()

    # -------------------------------------------------
    # Click Object with Retry + Timeout
    # -------------------------------------------------
    def click_object(
        self,
        action,
        override_x=None,
        override_y=None,
        timeout=20,
        retry_interval=0.5,
        confidence=0.5
    ):

        """
        Try clicking object using image detection.
        Retry until timeout.

        If not found and fallback coordinates exist,
        click fallback position.
        """
        object_name = action.target
        if override_x is None or override_y is None:
            override_x = action.x
            override_y = action.y

        start_time = time.time()

        while time.time() - start_time < timeout:

            location = self.finder.find_object(object_name, confidence=confidence)

            if location:
                x, y = location

                print(f"smart_click::click_object() - Object '{object_name}' found at {x},{y}")

                pyautogui.moveTo(x, y)
                pyautogui.click()
                return True

            time.sleep(retry_interval)

        # fallback coordinate click
        if override_x is not None and override_y is not None:
            print(f"Fallback click at {override_x},{override_y}")
            pyautogui.moveTo(override_x, override_y)
            pyautogui.click()
            return True

        # failure
        raise Exception(
            f"Object '{object_name}' not found within {timeout} seconds"
        )
