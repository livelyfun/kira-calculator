"""Standard arithmetic calculator keypad page."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QGridLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class StandardPage(QWidget):
    """Keypad for standard daily arithmetic calculations."""

    button_clicked = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.buttons: dict[str, QPushButton] = {}
        self._create_ui()

    def _create_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        grid = QGridLayout()
        grid.setSpacing(8)

        button_layout = [
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

        for text, row, col, obj_name in button_layout:
            btn = QPushButton(text)
            btn.setObjectName(obj_name)
            btn.clicked.connect(lambda checked=False, t=text: self.button_clicked.emit(t))
            grid.addWidget(btn, row, col)
            self.buttons[text] = btn

        layout.addLayout(grid)

