from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class ConverterPage(QWidget):
    """Dedicated placeholder boundary for the future unit-converter UI."""

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Unit Converter")
        title.setObjectName("converterTitle")
        description = QLabel("Unit conversion will be available in a future release.")
        description.setObjectName("converterDescription")

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addStretch()
