import sys
import os
import json

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QPushButton, QLineEdit, QDialog
)

from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtGui import QPainter, QColor, QPen, QPixmap, QImage

import mss
import numpy as np
from PIL import Image
from src.object_repo.object_manager import ObjectRepositoryManager

class SnipPopup(QDialog):

    def __init__(self, screenshot, rect):
        super().__init__()

        self.screenshot = screenshot
        self.rect = rect

        self.setWindowTitle("Save Object")

        layout = QVBoxLayout()

        # Convert numpy -> QPixmap
        h, w, ch = screenshot.shape
        qimg = QImage(screenshot.data, w, h, ch * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)

        img_label = QLabel()
        img_label.setPixmap(pixmap)
        layout.addWidget(img_label)

        coord = f"x:{rect.left()}  y:{rect.top()}  w:{rect.width()}  h:{rect.height()}"
        layout.addWidget(QLabel(coord))

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter object name")
        layout.addWidget(self.name_edit)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_object)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    # ---------------------------------------------------
    # Save object to repository
    # ---------------------------------------------------
    def save_object(self):

        name = self.name_edit.text().strip()

        if not name:
            return

        try:
            manager = ObjectRepositoryManager()
            manager.save_object(name, self.screenshot, self.rect)

            self.accept()
        except Exception as e:
            print(e)