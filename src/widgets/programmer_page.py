from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class ProgrammerPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        label = QLabel("Programmer Mode\n\nComing Soon")
        label.setStyleSheet("""
            color:white;
            font-size:28px;
        """)

        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()