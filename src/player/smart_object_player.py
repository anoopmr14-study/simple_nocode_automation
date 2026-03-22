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


class SmartObjectPlayer:

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

        Reliable object click with:
        - Image detection
        - Retry + timeout
        - Region-based optimization
        - Fallback coordinates
        """

        object_name = action.target

        # -------------------------------------------------
        # Prepare fallback coordinates
        # -------------------------------------------------
        if override_x is None:
            override_x = action.x

        if override_y is None:
            override_y = action.y

        # -------------------------------------------------
        # Find object using shared retry logic
        # -------------------------------------------------
        location = self._find_with_retry(
            action=action,
            timeout=timeout,
            retry_interval=retry_interval,
            confidence=confidence
        )

        # -------------------------------------------------
        # If found → Click
        # -------------------------------------------------
        if location:
            x, y = location
            print(f"smart_object_player::click_object() -  '{object_name}' found at {x},{y} and click triggered")

            pyautogui.moveTo(x, y)
            pyautogui.click()
            return True

        # -------------------------------------------------
        # Fallback click
        # -------------------------------------------------
        if override_x is not None and override_y is not None:
            print(f"smart_object_player::click_object() - Fallback click at {override_x},{override_y}")

            pyautogui.moveTo(override_x, override_y)
            pyautogui.click()
            return True

        # -------------------------------------------------
        # Failure
        # -------------------------------------------------
        raise Exception(
            f"smart_object_player::click_object() - Object '{object_name}' not found within {timeout} seconds"
        )


    def validate_object(self, action, timeout=5, confidence=0.5):
        """
        Validate if object exists on screen.
        Returns True/False (NO click).
        """
        location = self._find_with_retry(
            action,
            timeout=timeout,
            retry_interval=0.5,
            confidence=confidence
        )

        if location:
            print(f"[VALIDATE] Object '{action.target}' FOUND")
            return True
        else:
            print(f"[VALIDATE] Object '{action.target}' NOT FOUND")
            return False

    def wait_for_object(self, action, timeout=None, confidence=0.5):
        """
        Wait until object appears.
        Uses action.delay as timeout.
        """
        if timeout is None:
            timeout = action.delay if action.delay > 0 else 10

        location = self._find_with_retry(
            action,
            timeout=timeout,
            retry_interval=0.5,
            confidence=confidence
        )

        if location:
            print(f"[WAIT] Object '{action.target}' appeared")
            return True

        raise Exception(
            f"[WAIT FAILED] Object '{action.target}' not found in {timeout} seconds"
        )

    def _find_with_retry(self, action, timeout, retry_interval, confidence):
        object_name = action.target
        start_time = time.time()

        while time.time() - start_time < timeout:
            location = self.finder.find_object(object_name, confidence=confidence)

            if location:
                return location

            time.sleep(retry_interval)

        return None