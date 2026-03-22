# src/ui/step_editor_dialog.py

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox,
    QLineEdit, QPushButton, QHBoxLayout
)

from src.core.action import Action
from src.object_repo.object_manager import ObjectRepositoryManager


class StepEditorDialog(QDialog):

    # -------------------------------------------------
    # Initialize dialog with optional existing action to edit
    # -------------------------------------------------
    def __init__(self, parent=None, action=None):
        super().__init__(parent)

        self.setWindowTitle("Step Editor")
        self.setMinimumWidth(300)

        self.repo = ObjectRepositoryManager()
        self.action = action

        self.init_ui()
        self.load_objects_dropdown()

        if action:
            self.load_action(action)

    # -------------------------------------------------
    # Init UI components
    # -------------------------------------------------
    def init_ui(self):

        layout = QVBoxLayout()

        # Action type
        layout.addWidget(QLabel("Action Type"))
        self.action_type = QComboBox()
        self.action_type.addItems([
            "Mouse Move", "Click Object", "Validate Object", "Wait Object", "Click", "Right Click", "Double Click",
            "Type", "Hotkey", "Key", "Wait"
        ])
        layout.addWidget(self.action_type)

        # Object dropdown
        layout.addWidget(QLabel("Object"))
        self.object_dropdown = QComboBox()
        layout.addWidget(self.object_dropdown)

        # Coordinates
        layout.addWidget(QLabel("X- Co-oridnate"))
        self.x_input = QLineEdit()
        layout.addWidget(self.x_input)

        layout.addWidget(QLabel("Y- Co-oridnate"))
        self.y_input = QLineEdit()
        layout.addWidget(self.y_input)

        layout.addWidget(QLabel("Width"))
        self.w_input = QLineEdit()
        layout.addWidget(self.w_input)

        layout.addWidget(QLabel("Height"))
        self.h_input = QLineEdit()
        layout.addWidget(self.h_input)

        # Text
        layout.addWidget(QLabel("Text"))
        self.text_input = QLineEdit()
        layout.addWidget(self.text_input)

        # Delay
        layout.addWidget(QLabel("Delay (seconds)"))
        self.delay_input = QLineEdit()
        layout.addWidget(self.delay_input)

        # Buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")

        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # events
        self.save_btn.clicked.connect(self.save_action)
        self.cancel_btn.clicked.connect(self.reject)
        self.action_type.currentTextChanged.connect(self.update_on_action_type_change)
        self.object_dropdown.currentTextChanged.connect(self.update_on_object_change)

        # For initial state
        self.update_on_action_type_change()
        self.update_on_object_change()

    # -------------------------------------------------
    # Load objects from repository to dropdown
    # -------------------------------------------------
    def load_objects_dropdown(self):
        objects = self.repo.list_objects()
        self.object_dropdown.addItems(objects)

    # -------------------------------------------------
    # Load existing action data into dialog fields for editing
    # -------------------------------------------------
    def load_action(self, action):
        self.action_type.setCurrentText(action.action_type)

        if action.target:
            self.object_dropdown.setCurrentText(action.target)

        if action.x:
            self.x_input.setText(str(action.x))

        if action.y:
            self.y_input.setText(str(action.y))

        if action.w:
            self.x_input.setText(str(action.w))

        if action.h:
            self.y_input.setText(str(action.h))

        if action.text:
            self.text_input.setText(action.text)

        if action.delay:
            self.delay_input.setText(str(action.delay))

    # -------------------------------------------------
    # Save action from dialog fields and return Action object to caller
    # -------------------------------------------------
    def save_action(self):

        action_type = self.action_type.currentText()

        x = int(self.x_input.text()) if self.x_input.text() else None
        y = int(self.y_input.text()) if self.y_input.text() else None
        w = int(self.w_input.text()) if self.w_input.text() else None
        h = int(self.h_input.text()) if self.h_input.text() else None
        text = self.text_input.text() or None
        delay = float(self.delay_input.text()) if self.delay_input.text() else 0.0

        target = None
        if action_type in ["object_click", "Click Object", "validate_object", "Validate Object", "wait_Object", "Wait Object" ]:
            target = self.object_dropdown.currentText()

        self.result_action = Action(
            action_type=action_type,
            target=target,
            x=x,
            y=y,
            w=w,
            h=h,
            text=text,
            delay=delay
        )
        print("Saved Action:", self.result_action.to_dict())

        self.accept()

    # -------------------------------------------------
    # Get the resulting Action object after dialog is accepted
    # -------------------------------------------------
    def get_action(self):
        return getattr(self, "result_action", None)

    # -------------------------------------------------
    # Update enabled/disabled fields based on selected action type
    # -------------------------------------------------  
    def update_on_action_type_change(self):
        action_type = self.action_type.currentText()

        # Clear all fields except action type and view
        self.clear_all_fields()

        # Reset all
        self.object_dropdown.setEnabled(False)
        # self.x_input.setVisible(False)
        self.x_input.setEnabled(False)
        self.y_input.setEnabled(False)
        self.w_input.setEnabled(False)
        self.h_input.setEnabled(False)
        self.text_input.setEnabled(False)
        self.delay_input.setEnabled(False)

        if action_type in ["object_click", "Click Object", "validate_object", "Validate Object", "wait_Object", "Wait Object" ]:
            self.object_dropdown.setEnabled(True)
            self.x_input.setEnabled(True)
            self.y_input.setEnabled(True)
            self.w_input.setEnabled(True)
            self.h_input.setEnabled(True)
            self.update_on_object_change()  # to populate coordinates if object selected

            if action_type in ["wait_Object", "Wait Object"]:
                self.delay_input.setEnabled(True)

        elif action_type in ["mouse_move", "Mouse Move", "click", "Click", "right_click", "Right Click", "double_click", "Double Click"]:
            self.x_input.setEnabled(True)
            self.y_input.setEnabled(True)


        elif action_type in ["type", "Type", "hotkey", "Hotkey", "key", "Key"]:
            self.text_input.setEnabled(True)

        elif action_type in ["wait", "Wait"]:
            self.delay_input.setEnabled(True)
    # -------------------------------------------------
    # Update enabled/disabled fields based on selected action type
    # -------------------------------------------------  
    def update_on_object_change(self):
        if self.action_type.currentText() not in ["object_click", "Click Object", "validate_object", "Validate Object", "wait_Object", "Wait Object"]:
            return
        
        object_name = self.object_dropdown.currentText()
        obj = self.repo.get_object(object_name)

        if obj:
            self.x_input.setText(str(obj.get("x")))
            self.y_input.setText(str(obj.get("y")))
            self.w_input.setText(str(obj.get("w")))
            self.h_input.setText(str(obj.get("h")))

    def clear_all_fields(self):
        self.x_input.clear()
        self.y_input.clear()
        self.w_input.clear()
        self.h_input.clear()
        self.text_input.clear()
        self.delay_input.clear()