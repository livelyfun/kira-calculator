from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout


class ModeBar(QWidget):

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)

        self.calculator_button = QPushButton("Calculator")
        self.programmer_button = QPushButton("Programmer")
        self.converter_button = QPushButton("Converter")

        buttons = [
            self.calculator_button,
            self.programmer_button,
            self.converter_button,
        ]

        for button in buttons:
            button.setCheckable(True)
            layout.addWidget(button)

        self.calculator_button.setChecked(True)