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
from src.ui.step_editor_dialog import StepEditorDialog

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
        self.add_step_btn = QPushButton("Add Step")
        self.delete_btn = QPushButton("Delete")
        self.up_btn = QPushButton("Up")
        self.down_btn = QPushButton("Down")
        self.dup_btn = QPushButton("Duplicate")
        self.insert_obj_btn = QPushButton("Insert Object")
        self.play_btn = QPushButton("Play")
        self.load_btn = QPushButton("Load")
        self.save_btn = QPushButton("Save")

        button_layout.addWidget(self.record_btn)
        button_layout.addWidget(self.add_step_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.up_btn)
        button_layout.addWidget(self.down_btn)
        button_layout.addWidget(self.dup_btn)
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
        self.add_step_btn.clicked.connect(self.open_step_editor)
        self.delete_btn.clicked.connect(self.delete_step)
        self.up_btn.clicked.connect(self.move_up)
        self.down_btn.clicked.connect(self.move_down)
        self.dup_btn.clicked.connect(self.duplicate_step)
        self.insert_obj_btn.clicked.connect(self.capture_object)
        self.play_btn.clicked.connect(self.play_workflow)
        self.load_btn.clicked.connect(self.load_file)
        self.save_btn.clicked.connect(self.save_file)
        self.step_list.itemDoubleClicked.connect(self.edit_step)

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
    # open step editor dialog to add a new step manually
    # -------------------------------------------------
    def open_step_editor(self):
        dialog = StepEditorDialog(self)

        if dialog.exec():
            action = dialog.get_action()
            if action:
                self.workflow.add_action(action)
                self.refresh_workflow_list()

    # -------------------------------------------------
    # Edit Step - open step editor dialog with existing action data for editing
    # -------------------------------------------------
    def edit_step(self, item):
        index = self.step_list.row(item)
        action = self.workflow.get_actions()[index]

        dialog = StepEditorDialog(self, action)
        if dialog.exec():
            self.workflow.actions[index] = dialog.get_action()
            self.refresh_workflow_list()

    # -------------------------------------------------
    # Delete Step - removes selected step from workflow and updates UI
    # -------------------------------------------------
    def delete_step(self):
        index = self.step_list.currentRow()
        if index >= 0:
            self.workflow.delete_action(index)
            self.refresh_workflow_list()

    # -------------------------------------------------
    # Move Up - moves selected step up in workflow and updates UI
    # -------------------------------------------------
    def move_up(self):
        i = self.step_list.currentRow()
        self.workflow.move_up(i)
        self.refresh_workflow_list()
        self.step_list.setCurrentRow(max(0, i - 1))

    # -------------------------------------------------
    # Move Down - moves selected step down in workflow and updates UI
    # -------------------------------------------------
    def move_down(self):
        i = self.step_list.currentRow()
        self.workflow.move_down(i)
        self.refresh_workflow_list()
        self.step_list.setCurrentRow(i + 1)

    # -------------------------------------------------
    # Duplicate Step - creates a copy of the selected step in the workflow and updates UI
    # -------------------------------------------------
    def duplicate_step(self):
        from copy import deepcopy
        i = self.step_list.currentRow()
        if i >= 0:
            action = self.workflow.get_actions()[i]
            self.workflow.actions.insert(i + 1, deepcopy(action))
            self.refresh_workflow_list()

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