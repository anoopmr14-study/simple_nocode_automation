
import os
import sys
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()