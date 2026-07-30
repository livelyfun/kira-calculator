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

app = QApplication(sys.argv)

# Load stylesheet
with open("src/styles/main.qss", "r") as file:
    app.setStyleSheet(file.read())

# -----------------------
# Main Window
# -----------------------

window = QMainWindow()
window.setWindowTitle("Kira Calculator")
window.resize(400, 600)

# -----------------------
# Central Widget
# -----------------------

central_widget = QWidget()
window.setCentralWidget(central_widget)

# -----------------------
# Main Layout
# -----------------------

layout = QVBoxLayout()
layout.setSpacing(15)
layout.setContentsMargins(15, 15, 15, 15)

central_widget.setLayout(layout)

# -----------------------
# Display
# -----------------------

display = QLabel("0")

display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

display.setMinimumHeight(100)

display.setSizePolicy(
    QSizePolicy.Policy.Expanding,
    QSizePolicy.Policy.Fixed,
)

layout.addWidget(display)

# -----------------------
# Button Grid
# -----------------------

grid = QGridLayout()
grid.setSpacing(10)

layout.addLayout(grid)

layout.setStretch(0, 0)
layout.setStretch(1, 1)

buttons = [
    "7", "8", "9", "÷",
    "4", "5", "6", "×",
    "1", "2", "3", "-",
    "C", "0", "=", "+",
]


def button_clicked(text):
    current = display.text()

    if current == "0":
        display.setText(text)
    else:
        display.setText(current + text)


for index, text in enumerate(buttons):

    button = QPushButton(text)

    button.clicked.connect(
        lambda checked=False, t=text: button_clicked(t)
    )

    row = index // 4
    column = index % 4

    grid.addWidget(button, row, column)

for row in range(4):
    grid.setRowStretch(row, 1)

for column in range(4):
    grid.setColumnStretch(column, 1)

window.show()

app.exec()