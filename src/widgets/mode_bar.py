from PySide6.QtWidgets import QButtonGroup, QHBoxLayout, QPushButton, QWidget


class ModeBar(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        self.calculator_button = QPushButton("Calculator")
        self.programmer_button = QPushButton("Programmer")
        self.converter_button = QPushButton("Converter")

        buttons = [
            self.calculator_button,
            self.programmer_button,
            self.converter_button,
        ]

        for i, button in enumerate(buttons):
            button.setCheckable(True)
            self.button_group.addButton(button, i)
            layout.addWidget(button)

        self.calculator_button.setChecked(True)
