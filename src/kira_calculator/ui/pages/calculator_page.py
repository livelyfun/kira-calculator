"""Scientific + basic calculator keypad."""

from __future__ import annotations

from PySide6.QtWidgets import QGridLayout, QPushButton, QVBoxLayout, QWidget


class CalculatorPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.buttons: dict[str, QPushButton] = {}

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(10)

        root.addLayout(self._create_scientific_grid())
        root.addLayout(self._create_basic_grid())

    def _create_scientific_grid(self) -> QGridLayout:
        grid = QGridLayout()
        grid.setSpacing(6)

        buttons = [
            ("sin", 0, 0),
            ("cos", 0, 1),
            ("tan", 0, 2),
            ("log", 0, 3),
            ("ln", 0, 4),
            ("√", 1, 0),
            ("π", 1, 1),
            ("e", 1, 2),
            ("x²", 1, 3),
            ("xʸ", 1, 4),
            ("(", 2, 0),
            (")", 2, 1),
            ("%", 2, 2),
            ("±", 2, 3),
            ("1/x", 2, 4),
        ]

        for text, row, col in buttons:
            btn = QPushButton(text)
            btn.setObjectName("scientificButton")
            self.buttons[text] = btn
            grid.addWidget(btn, row, col)

        return grid

    def _create_basic_grid(self) -> QGridLayout:
        grid = QGridLayout()
        grid.setSpacing(8)

        buttons = [
            ("C", 0, 0),
            ("⌫", 0, 1),
            ("÷", 0, 2),
            ("×", 0, 3),
            ("7", 1, 0),
            ("8", 1, 1),
            ("9", 1, 2),
            ("-", 1, 3),
            ("4", 2, 0),
            ("5", 2, 1),
            ("6", 2, 2),
            ("+", 2, 3),
            ("1", 3, 0),
            ("2", 3, 1),
            ("3", 3, 2),
            ("=", 3, 3),
            ("0", 4, 0),
            (".", 4, 2),
        ]

        for text, row, col in buttons:
            btn = QPushButton(text)
            self.buttons[text] = btn

            if text.isdigit() or text == ".":
                btn.setObjectName("numberButton")
            elif text in {"+", "-", "×", "÷"}:
                btn.setObjectName("operatorButton")
            elif text == "=":
                btn.setObjectName("equalsButton")
            elif text == "⌫":
                btn.setObjectName("backspaceButton")
            elif text == "C":
                btn.setObjectName("clearButton")

            if text == "0":
                grid.addWidget(btn, row, col, 1, 2)
            else:
                grid.addWidget(btn, row, col)

        return grid
