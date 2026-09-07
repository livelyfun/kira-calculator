"""Scientific calculator controls layered on top of the standard keypad."""

from PySide6.QtWidgets import QComboBox, QGridLayout, QPushButton

from .calculator_page import CalculatorPage


class ScientificPage(CalculatorPage):
    """A standard keypad plus scientific functions and an angle-mode selector."""

    def __init__(self) -> None:
        super().__init__()
        self._create_scientific_controls()

    def _create_scientific_controls(self) -> None:
        self.angle_selector = QComboBox()
        self.angle_selector.setObjectName("angleSelector")
        self.angle_selector.addItems(["DEG", "RAD", "GRAD"])
        self.angle_selector.setCurrentText("DEG")
        self.layout.insertWidget(0, self.angle_selector)

        scientific_grid = QGridLayout()
        scientific_grid.setSpacing(6)
        buttons = [
            ("sin", 0, 0),
            ("cos", 0, 1),
            ("tan", 0, 2),
            ("asin", 0, 3),
            ("acos", 0, 4),
            ("atan", 1, 0),
            ("sinh", 1, 1),
            ("cosh", 1, 2),
            ("tanh", 1, 3),
            ("log", 1, 4),
            ("ln", 2, 0),
            ("√", 2, 1),
            ("π", 2, 2),
            ("e", 2, 3),
            ("x²", 2, 4),
            ("xʸ", 3, 0),
            ("%", 3, 1),
            ("!", 3, 2),
            ("±", 3, 3),
            ("1/x", 3, 4),
        ]

        for text, row, column in buttons:
            button = QPushButton(text)
            button.setObjectName("scientificButton")
            self.buttons[text] = button
            scientific_grid.addWidget(button, row, column)

        self.layout.insertLayout(1, scientific_grid)
