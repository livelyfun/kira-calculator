"""Standard calculator keypad."""

from PySide6.QtWidgets import QGridLayout, QPushButton, QVBoxLayout, QWidget


class CalculatorPage(QWidget):
    """Normal arithmetic controls used by the Standard calculator mode."""

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)

        self.buttons = {}

        self.create_basic_grid()

    def create_basic_grid(self):

        basic_grid = QGridLayout()
        basic_grid.setSpacing(8)

        buttons = [
            ("C", 0, 0),
            ("⌫", 0, 1),
            ("÷", 0, 2),
            ("×", 0, 3),
            ("(", 1, 0),
            (")", 1, 1),
            ("7", 1, 2),
            ("8", 1, 3),
            ("9", 2, 0),
            ("-", 2, 1),
            ("4", 2, 2),
            ("5", 2, 3),
            ("6", 3, 0),
            ("+", 3, 1),
            ("1", 3, 2),
            ("2", 3, 3),
            ("3", 4, 0),
            ("=", 4, 1),
            ("0", 4, 2),
            (".", 4, 3),
        ]

        for text, row, column in buttons:
            button = QPushButton(text)

            self.buttons[text] = button

            if text.isdigit() or text == ".":
                button.setObjectName("numberButton")

            elif text in ["+", "-", "×", "÷"]:
                button.setObjectName("operatorButton")

            elif text == "=":
                button.setObjectName("equalsButton")

            elif text == "⌫":
                button.setObjectName("backspaceButton")

            elif text == "C":
                button.setObjectName("clearButton")

            if text == "0":
                basic_grid.addWidget(
                    button,
                    row,
                    column,
                    1,
                    1,
                )
            else:
                basic_grid.addWidget(
                    button,
                    row,
                    column,
                )

        self.layout.addLayout(basic_grid)
