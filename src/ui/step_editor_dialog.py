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
        self.load_objects()

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
            "click", "right_click", "double_click",
            "object_click", "type", "wait"
        ])
        layout.addWidget(self.action_type)

        # Object dropdown
        layout.addWidget(QLabel("Object"))
        self.object_dropdown = QComboBox()
        layout.addWidget(self.object_dropdown)

        # Coordinates
        layout.addWidget(QLabel("X, Y"))
        self.x_input = QLineEdit()
        self.y_input = QLineEdit()
        layout.addWidget(self.x_input)
        layout.addWidget(self.y_input)

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

    # -------------------------------------------------
    # Load objects from repository to dropdown
    # -------------------------------------------------
    def load_objects(self):
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
        text = self.text_input.text() or None
        delay = float(self.delay_input.text()) if self.delay_input.text() else 0.0

        target = None
        if action_type == "object_click":
            target = self.object_dropdown.currentText()

        self.result_action = Action(
            action_type=action_type,
            target=target,
            x=x,
            y=y,
            text=text,
            delay=delay
        )

        self.accept()

    # -------------------------------------------------
    # Get the resulting Action object after dialog is accepted
    # -------------------------------------------------
    def get_action(self):
        return getattr(self, "result_action", None)