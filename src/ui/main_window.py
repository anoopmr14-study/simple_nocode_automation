"""
Main Workflow Editor UI
"""

import sys
import threading
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget,
    QFileDialog, QMessageBox
)

from src.recorder.action_recorder import ActionRecorder
from src.player.action_player import ActionPlayer


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple UI Automation Tool")
        self.resize(700, 500)

        self.recorder = ActionRecorder()
        self.player = ActionPlayer()

        self.init_ui()

    # -------------------------------------------------
    # Build UI
    # -------------------------------------------------
    def init_ui(self):

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # -----------------------------
        # Buttons
        # -----------------------------
        button_layout = QHBoxLayout()

        self.record_btn = QPushButton("Record")
        self.play_btn = QPushButton("Play")
        self.load_btn = QPushButton("Load")
        self.save_btn = QPushButton("Save")

        button_layout.addWidget(self.record_btn)
        button_layout.addWidget(self.play_btn)
        button_layout.addWidget(self.load_btn)
        button_layout.addWidget(self.save_btn)

        # -----------------------------
        # Workflow Step List
        # -----------------------------
        self.step_list = QListWidget()

        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.step_list)

        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

        # -----------------------------
        # Connect Events
        # -----------------------------
        self.record_btn.clicked.connect(self.start_recording)
        self.play_btn.clicked.connect(self.play_workflow)
        self.load_btn.clicked.connect(self.load_file)
        self.save_btn.clicked.connect(self.save_file)

    # -------------------------------------------------
    # Start Recording in thread to avoid blocking UI
    # -------------------------------------------------
    def start_recording(self):

        QMessageBox.information(
            self,
            "Recording",
            "Recording started.\nPress Ctrl+Alt+S to stop."
        )

        # hide automation UI
        self.hide()

        thread = threading.Thread(target=self.run_recording)
        thread.start()

    # -------------------------------------------------
    # Recording Logic - runs in separate thread
    # -------------------------------------------------
    def run_recording(self):

        self.recorder.start_recording()

        # show UI again
        self.show()

        self.step_list.clear()

        for action in self.recorder.actions:
            self.step_list.addItem(action)   


    # -------------------------------------------------
    # Play Automation   - runs in separate thread to avoid blocking UI
    # -------------------------------------------------
    def play_workflow(self):

        if self.step_list.count() == 0:
            QMessageBox.warning(self, "Error", "No steps available")
            return

        actions = []

        for i in range(self.step_list.count()):
            actions.append(self.step_list.item(i).text())

        temp_file = "temp_playback.txt"

        with open(temp_file, "w") as f:
            for action in actions:
                f.write(action + "\n")

        # hide UI
        self.hide()

        # run playback in separate thread to avoid blocking UI
        thread = threading.Thread(
            target=self.run_playback,
            args=(temp_file,)
        )
        thread.start()

    # -------------------------------------------------
    # Run Playback Logic - runs in separate thread
    # -------------------------------------------------
    def run_playback(self, file):

        self.player.play_file(file)

        # show UI when playback finishes
        self.show()

    # -------------------------------------------------
    # Load File
    # -------------------------------------------------
    def load_file(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Recording",
            "",
            "Text Files (*.txt)"
        )

        if not file_path:
            return

        self.step_list.clear()

        with open(file_path, "r") as f:
            for line in f:
                self.step_list.addItem(line.strip())

    # -------------------------------------------------
    # Save File
    # -------------------------------------------------
    def save_file(self):

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Recording",
            "",
            "Text Files (*.txt)"
        )

        if not file_path:
            return

        with open(file_path, "w") as f:

            for i in range(self.step_list.count()):
                action = self.step_list.item(i).text()
                f.write(action + "\n")

        QMessageBox.information(self, "Saved", "Workflow saved successfully")