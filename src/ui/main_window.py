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

from src.core.workflow_manager import WorkflowManager
from src.core.action import Action

from src.recorder.action_recorder import ActionRecorder
from src.player.action_player import ActionPlayer

from src.snipping.snipping_overlay import SnippingOverlayWindow
from src.snipping.snipping_popup import SnipPopup


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple UI Automation Tool")
        self.resize(700, 500)

        self.workflow = WorkflowManager()
        self.recorder = ActionRecorder(callback=self.add_recorded_action,
                                        stop_callback=self.on_recording_stopped)

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
        self.insert_obj_btn = QPushButton("Insert Object")
        self.play_btn = QPushButton("Play")
        self.load_btn = QPushButton("Load")
        self.save_btn = QPushButton("Save")

        button_layout.addWidget(self.record_btn)
        button_layout.addWidget(self.insert_obj_btn)
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
        self.insert_obj_btn.clicked.connect(self.capture_object)
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

        # self.step_list.clear()

        # for action in self.recorder.actions:
        #     self.step_list.addItem(action)   

    # -------------------------------------------------
    # Stop Recording - callback from recorder when recording is stopped to update UI
    # -------------------------------------------------
    def on_recording_stopped(self):
        self.show()
        self.refresh_workflow_list()

    # -------------------------------------------------
    # Add Recorded Action - callback from recorder to add action to workflow and update UI
    # -------------------------------------------------   
    def add_recorded_action(self, action):
        self.workflow.add_action(action)
        self.refresh_workflow_list()

    # -------------------------------------------------
    # Refresh Workflow List - updates the UI list widget to reflect current workflow actions
    # -------------------------------------------------  
    def refresh_workflow_list(self):
        self.step_list.clear()
        for action in self.workflow.get_actions():
            self.step_list.addItem(str(action))

    # -------------------------------------------------
    # Capture Object using Snipping Tool
    # -------------------------------------------------
    def capture_object(self):

        # hide automation UI
        self.hide()

        self.snipping_tool = SnippingOverlayWindow()

        # receive screenshot result
        self.snipping_tool.snip_completed.connect(self.on_snip_complete)

        self.snipping_tool.show()

    # -------------------------------------------------
    # On Snip Complete - receive screenshot + rectangle from snipping tool
    # -------------------------------------------------
    def on_snip_complete(self, screenshot, rect):

        # show Main UI again
        self.show()
        self.raise_()
        self.activateWindow()

        popup = SnipPopup(screenshot, rect)

        if popup.exec():
            print("Object saved")

            # object saved successfully
            name = popup.name_edit.text().strip()

            if name:
                self.insert_object_step(name)

    # -------------------------------------------------
    # Insert Object Step - adds a step to the workflow list for the captured object
    # -------------------------------------------------
    def insert_object_step(self, object_name):
        action = Action(
            action_type="object_click",
            target=object_name
        )
        self.workflow.add_action(action)
        self.refresh_workflow_list()

    # -------------------------------------------------
    # Play Automation   - runs in separate thread to avoid blocking UI
    # -------------------------------------------------
    def play_workflow(self):

        if not self.workflow.get_actions():
            QMessageBox.warning(self, "Error", "No steps available")
            return

        # hide UI
        self.hide()

        # run playback in separate thread to avoid blocking UI
        thread = threading.Thread(target=self.run_playback)
        thread.start()

    # -------------------------------------------------
    # Run Playback Logic - runs in separate thread
    # -------------------------------------------------
    def run_playback(self):
        player = ActionPlayer(self.workflow.get_actions())
        player.play()

        # show UI when playback finishes
        self.show()
        # from PySide6.QtCore import QTimer
        # QTimer.singleShot(0, self.show)

    # -------------------------------------------------
    # Load File
    # -------------------------------------------------
    def load_file(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Workflow",
            "",
            "JSON Files (*.json)"
        )

        if not file_path:
            return
        
        self.workflow.load(file_path)
        self.refresh_workflow_list()

    # -------------------------------------------------
    # Save File
    # -------------------------------------------------
    def save_file(self):

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Workflow",
            "workflow.json",
            "JSON Files (*.json)"
        )

        if not file_path:
            return
        
        path = self.workflow.save(file_path)
        QMessageBox.information(self, "Saved Workflow: ", "Workflow saved successfully: " + str(path))