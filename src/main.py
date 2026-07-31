import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

class CalculatorWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kira Calculator")
        self.resize(400, 600)

        self.create_ui()

    def create_ui(self):

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Layout
        layout = QVBoxLayout()

        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        central_widget.setLayout(layout)

        # Display
        self.display = QLabel("0")

        self.display.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.display.setMinimumHeight(100)

        self.display.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        layout.addWidget(self.display)

        # Grid
        grid = QGridLayout()

        grid.setSpacing(10)

        layout.addLayout(grid)

        buttons = [
            "7", "8", "9", "÷",
            "4", "5", "6", "×",
            "1", "2", "3", "-",
            "C", "0", "=", "+",
        ]

        for index, text in enumerate(buttons):

            button = QPushButton(text)

            button.clicked.connect(
                lambda checked=False, t=text: self.button_clicked(t)
            )

            row = index // 4
            column = index % 4

            grid.addWidget(button, row, column)

        for row in range(4):
            grid.setRowStretch(row, 1)

        for column in range(4):
            grid.setColumnStretch(column, 1)

    def button_clicked(self, text):

        current = self.display.text()

        if current == "0":
            self.display.setText(text)

        else:
            self.display.setText(current + text)


def main():

    app = QApplication(sys.argv)

    with open("src/styles/main.qss") as file:
        app.setStyleSheet(file.read())

    window = CalculatorWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()