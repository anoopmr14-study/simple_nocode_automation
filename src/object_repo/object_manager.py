"""
Object Repository Manager

Responsible for managing captured UI objects.

This class handles:
- saving objects
- loading objects
- retrieving objects
- deleting objects

All file operations for object repository must go through this manager.
"""

import os
import json
from PIL import Image


class ObjectRepositoryManager:

    def __init__(self,
                 mapping_file="results/objects/objectmapping.json",
                 object_dir="results/objects"):

        self.mapping_file = mapping_file
        self.object_dir = object_dir

        # ensure directories exist
        os.makedirs(self.object_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.mapping_file), exist_ok=True)

        # load existing objects
        self.objects = self.load_objects()

    # ---------------------------------------------------
    # Load objects from JSON file
    # ---------------------------------------------------
    def load_objects(self):

        if not os.path.exists(self.mapping_file):
            return {}

        try:
            with open(self.mapping_file, "r") as f:
                data = json.load(f)

            return data

        except Exception as e:
            print("Error loading object repository:", e)
            return {}

    # ---------------------------------------------------
    # Save JSON mapping file
    # ---------------------------------------------------
    def save_mapping(self):
        with open(self.mapping_file, "w") as f:
            json.dump(self.objects, f, indent=4)

    # ---------------------------------------------------
    # Add / Save object
    # ---------------------------------------------------
    def save_object(self, name, screenshot, rect):

        """
        Save captured object

        name : object name
        screenshot : numpy image
        rect : QRect containing coordinates
        """

        # prevent duplicate names
        if name in self.objects:
            raise ValueError(f"Object '{name}' already exists")

        image_path = os.path.join(self.object_dir, f"{name}.png")

        # save image
        Image.fromarray(screenshot).save(image_path)

        self.objects[name] = {
            "name": name,
            "image": image_path,
            "x": rect.left(),
            "y": rect.top(),
            "w": rect.width(),
            "h": rect.height()
        }

        self.save_mapping()

    # ---------------------------------------------------
    # Get object
    # ---------------------------------------------------
    def get_object(self, name):

        return self.objects.get(name)

    # ---------------------------------------------------
    # Delete object
    # ---------------------------------------------------
    def delete_object(self, name):

        if name not in self.objects:
            return False

        image_path = self.objects[name]["image"]

        # remove image file
        if os.path.exists(image_path):
            os.remove(image_path)

        del self.objects[name]

        self.save_mapping()

        return True

    # ---------------------------------------------------
    # List all objects
    # ---------------------------------------------------
    def list_objects(self):
        return list(self.objects.keys())


# -------------------------------------------------------
# Independent Test Runner
# -------------------------------------------------------

if __name__ == "__main__":

    """
    Test the Object Repository Manager independently
    """

    import numpy as np
    from PySide6.QtCore import QRect

    manager = ObjectRepositoryManager()

    # create fake image
    test_image = np.zeros((100, 200, 3), dtype=np.uint8)

    rect = QRect(100, 200, 200, 100)

    try:
        manager.save_object("TestButton", test_image, rect)
        print("Object saved")

    except Exception as e:
        print(e)

    print("Available objects:", manager.list_objects())

    obj = manager.get_object("TestButton")

    print("Object details:", obj)