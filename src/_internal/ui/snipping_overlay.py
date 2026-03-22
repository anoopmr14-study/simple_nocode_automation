import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtGui import QPainter, QColor, QPen
import mss
import numpy as np
from PIL import Image

from .snipping_popup import SnipPopup



class SnippingOverlayWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.start = QPoint()
        self.end = QPoint()
        self.dragging = False
        self.screenshot = None

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)


        self.setWindowState(Qt.WindowFullScreen)
        self.setCursor(Qt.CrossCursor)

    # Mouse pressed
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start = event.pos()
            self.end = self.start
            self.dragging = True
            self.update()

    # Mouse move
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.end = event.pos()
            self.update()

    # Mouse released -> capture immediately
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.end = event.pos()
            self.dragging = False
            rect = QRect(self.start, self.end).normalized()

            self.capture(rect)

            self.hide()   # IMPORTANT: remove fullscreen overlay

            # Launch Snipping Popup to save the captured object
            popup = SnipPopup(self.screenshot, rect)
            popup.exec()

            # Close the overlay and not stop the Application
            #self.close()

            # Close the overlay and stop the Application
            QApplication.quit()

    # Draw overlay + rectangle
    def paintEvent(self, event):
        painter = QPainter(self)

        # Dark overlay
        #painter.fillRect(self.rect(), QColor(0, 0, 0, 100))
        # dim screen
        painter.fillRect(self.rect(), QColor(0, 0, 0, 120))   

        if self.dragging:
            rect = QRect(self.start, self.end).normalized()

            # Clear selected area
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.fillRect(rect, Qt.transparent)

            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

            # Border
            pen = QPen(QColor(0, 180, 255), 2)
            painter.setPen(pen)
            #painter.drawRect(rect)
            painter.drawRect(rect.adjusted(0,0,-1,-1))

    # Capture using MSS
    def capture(self, rect):
        x = rect.left()
        y = rect.top()
        w = rect.width()
        h = rect.height()

        with mss.mss() as sct:
            monitor = {"left": x, "top": y, "width": w, "height": h}
            img = sct.grab(monitor)

        img = Image.frombytes("RGB", img.size, img.rgb)
        self.screenshot = np.array(img)

        print("Captured:", self.screenshot.shape)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    overlay = SnippingOverlayWindow()
    overlay.show()

    sys.exit(app.exec())