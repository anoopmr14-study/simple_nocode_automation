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
        object_name,
        fallback_x=None,
        fallback_y=None,
        timeout=100,
        retry_interval=0.5
    ):

        """
        Try clicking object using image detection.
        Retry until timeout.

        If not found and fallback coordinates exist,
        click fallback position.
        """

        start_time = time.time()

        while time.time() - start_time < timeout:

            location = self.finder.find_object(object_name)

            if location:

                x, y = location

                print(f"Object '{object_name}' found at {x},{y}")

                pyautogui.moveTo(x, y)
                pyautogui.click()

                return True

            print(f"Retrying object search: {object_name}")

            time.sleep(retry_interval)

        # -----------------------------
        # fallback coordinate click
        # -----------------------------

        if fallback_x is not None and fallback_y is not None:

            print(
                f"Object '{object_name}' not found. "
                f"Using fallback coordinates."
            )

            pyautogui.moveTo(fallback_x, fallback_y)
            pyautogui.click()

            return True

        # -----------------------------
        # failure
        # -----------------------------

        raise Exception(
            f"Object '{object_name}' not found within {timeout} seconds"
        )