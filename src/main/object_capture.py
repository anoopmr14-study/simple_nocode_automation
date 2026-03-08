import os
import json
import cv2
import numpy as np
import mss

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QLineEdit, QDialog
)

from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QColor, QPainter, QPen, QPixmap


RESULT_DIR = "results"
OBJECT_DIR = os.path.join(RESULT_DIR, "objects")
MAP_FILE = os.path.join(RESULT_DIR, "objectmapping.json")

os.makedirs(OBJECT_DIR, exist_ok=True)


class ObjectCapture:

    def __init__(self, parent=None):
        self.parent = parent
        self.overlay = None

    def start_capture(self):
        self.overlay = SnippingOverlay(self.parent)
        self.overlay.showFullScreen()

        # Make overlay multi-monitor safe with Full Screen and stay on top flags
        #self.overlay.setGeometry(QApplication.primaryScreen().geometry())
        #self.overlay.show()

        self.overlay.raise_()
        self.overlay.activateWindow()

# ---------------------------
# Transparent Overlay
# ---------------------------
class SnippingOverlay(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        #self.setWindowOpacity(0.35)
        self.setWindowState(Qt.WindowFullScreen)
        self.setCursor(Qt.CrossCursor)

        self.start = None
        self.end = None

    def mousePressEvent(self, event):
        self.start = event.pos()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.end = event.pos()
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.capture_area()

    def paintEvent(self, event):

        if not self.start or not self.end:
            return

        painter = QPainter(self)
        # dim screen
        painter.fillRect(self.rect(), QColor(0, 0, 0, 120))   
        
        painter.setPen(QPen(Qt.red, 2))

        rect = QRect(self.start, self.end).normalized()
        #painter.drawRect(rect)
        painter.drawRect(rect.adjusted(0,0,-1,-1))

    # -------------------
    # Capture Screenshot
    # -------------------
    def capture_area(self):

        x1 = min(self.start.x(), self.end.x())
        y1 = min(self.start.y(), self.end.y())

        x2 = max(self.start.x(), self.end.x())
        y2 = max(self.start.y(), self.end.y())

        w = x2 - x1
        h = y2 - y1

        with mss.mss() as sct:
            monitor = {"top": y1, "left": x1, "width": w, "height": h}
            img = sct.grab(monitor)

        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        self.close()

        ObjectPreview(img, (x1, y1, w, h)).exec()

        # Restore Main UI After Capture
        if self.parent():
            self.parent().show()


# ---------------------------
# Preview Dialog
# ---------------------------
class ObjectPreview(QDialog):

    def __init__(self, img, coords):
        super().__init__()

        self.img = img
        self.coords = coords

        self.setWindowTitle("Save Object")

        layout = QVBoxLayout()

        # preview image
        height, width = img.shape[:2]

        qimg = QPixmap.fromImage(
            QPixmap.fromImage(
                QPixmap.fromImage
            )
        )

        qimg = QPixmap(width, height)
        qimg.loadFromData(cv2.imencode(".png", img)[1].tobytes())

        label = QLabel()
        label.setPixmap(qimg.scaled(300, 200, Qt.KeepAspectRatio))
        layout.addWidget(label)

        self.name_box = QLineEdit()
        self.name_box.setPlaceholderText("Enter Object Name")
        layout.addWidget(self.name_box)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_object)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    # -------------------
    # Save object
    # -------------------
    def save_object(self):

        name = self.name_box.text().strip()

        if not name:
            return

        img_path = os.path.join(OBJECT_DIR, f"{name}.png")

        cv2.imwrite(img_path, self.img)

        data = {}

        if os.path.exists(MAP_FILE):
            with open(MAP_FILE) as f:
                data = json.load(f)

        data[name] = {
            "image": img_path,
            "coords": self.coords
        }

        with open(MAP_FILE, "w") as f:
            json.dump(data, f, indent=4)

        self.accept()