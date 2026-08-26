from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class CalculatorPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)

        self.buttons = {}

        self.create_angle_selector()
        self.create_scientific_grid()
        self.create_basic_grid()

    def create_angle_selector(self):

        self.angle_selector = QComboBox()
        self.angle_selector.setObjectName("angleSelector")

        self.angle_selector.addItems(
            [
                "DEG",
                "RAD",
                "GRAD",
            ]
        )

        self.angle_selector.setCurrentText("DEG")

        self.layout.addWidget(self.angle_selector)

    def create_scientific_grid(self):

        scientific_grid = QGridLayout()
        scientific_grid.setSpacing(6)

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

        for text, row, column in buttons:
            button = QPushButton(text)
            button.setObjectName("scientificButton")

            self.buttons[text] = button

            scientific_grid.addWidget(
                button,
                row,
                column,
            )

        self.layout.addLayout(scientific_grid)

    def create_basic_grid(self):

        basic_grid = QGridLayout()
        basic_grid.setSpacing(8)

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
                    2,
                )
            else:
                basic_grid.addWidget(
                    button,
                    row,
                    column,
                )

        self.layout.addLayout(basic_grid)
