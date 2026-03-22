
import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main.auto_ui import SimpleAutomation
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleAutomation()
    window.show()
    sys.exit(app.exec())