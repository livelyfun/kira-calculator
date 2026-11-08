"""Scientific calculator keypad page with angle mode selector and advanced mathematical functions."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ScientificPage(QWidget):
    """Keypad for advanced scientific calculations."""

    button_clicked = Signal(str)
    angle_mode_changed = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.buttons: dict[str, QPushButton] = {}
        self._create_ui()

    def _create_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # Angle mode selector header
        angle_bar = QHBoxLayout()
        angle_bar.setContentsMargins(0, 0, 0, 2)
        angle_label = QLabel("Angle Mode:")
        angle_bar.addWidget(angle_label)

        self.angle_selector = QComboBox()
        self.angle_selector.setObjectName("angleSelector")
        self.angle_selector.addItems(["DEG", "RAD", "GRAD"])
        self.angle_selector.currentTextChanged.connect(self.angle_mode_changed.emit)
        angle_bar.addWidget(self.angle_selector)
        angle_bar.addStretch()
        layout.addLayout(angle_bar)

        # Scientific function grid
        sci_grid = QGridLayout()
        sci_grid.setSpacing(6)

        sci_buttons = [
            ("sin", 0, 0),
            ("cos", 0, 1),
            ("tan", 0, 2),
            ("log", 0, 3),
            ("ln", 0, 4),
            ("asin", 1, 0),
            ("acos", 1, 1),
            ("atan", 1, 2),
            ("√", 1, 3),
            ("xʸ", 1, 4),
            ("sinh", 2, 0),
            ("cosh", 2, 1),
            ("tanh", 2, 2),
            ("x²", 2, 3),
            ("1/x", 2, 4),
            ("π", 3, 0),
            ("e", 3, 1),
            ("!", 3, 2),
            ("(", 3, 3),
            (")", 3, 4),
        ]

        for text, row, col in sci_buttons:
            btn = QPushButton(text)
            btn.setObjectName("scientificButton")
            btn.clicked.connect(lambda checked=False, t=text: self.button_clicked.emit(t))
            sci_grid.addWidget(btn, row, col)
            self.buttons[text] = btn

        layout.addLayout(sci_grid)

        # Basic numerical & operator grid
        basic_grid = QGridLayout()
        basic_grid.setSpacing(6)

        basic_buttons = [
            ("C", 0, 0, "clearButton"),
            ("⌫", 0, 1, "backspaceButton"),
            ("%", 0, 2, "operatorButton"),
            ("÷", 0, 3, "operatorButton"),
            ("7", 1, 0, "numberButton"),
            ("8", 1, 1, "numberButton"),
            ("9", 1, 2, "numberButton"),
            ("×", 1, 3, "operatorButton"),
            ("4", 2, 0, "numberButton"),
            ("5", 2, 1, "numberButton"),
            ("6", 2, 2, "numberButton"),
            ("-", 2, 3, "operatorButton"),
            ("1", 3, 0, "numberButton"),
            ("2", 3, 1, "numberButton"),
            ("3", 3, 2, "numberButton"),
            ("+", 3, 3, "operatorButton"),
            ("±", 4, 0, "numberButton"),
            ("0", 4, 1, "numberButton"),
            (".", 4, 2, "numberButton"),
            ("=", 4, 3, "equalsButton"),
        ]

        for text, row, col, obj_name in basic_buttons:
            btn = QPushButton(text)
            btn.setObjectName(obj_name)
            btn.clicked.connect(lambda checked=False, t=text: self.button_clicked.emit(t))
            basic_grid.addWidget(btn, row, col)
            self.buttons[text] = btn

        layout.addLayout(basic_grid)

    def set_angle_mode(self, mode: str) -> None:
        self.angle_selector.setCurrentText(mode.upper())
