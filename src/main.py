import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QGridLayout,
)

app = QApplication(sys.argv)

with open("src/styles/main.qss", "r") as file:
    app.setStyleSheet(file.read())

window = QMainWindow()
window.setWindowTitle("Kira Calculator")
window.resize(400, 600)

# -----------------------
# Central Widget 
# -----------------------

central_widget = QWidget()

window.setCentralWidget(central_widget)

# ------------------------
# Layout
# ------------------------

layout = QVBoxLayout()

central_widget.setLayout(layout)

# -------------------------
# Display
# -------------------------

display = QLabel("0")
display.setStyleSheet("""
    font-size: 36px;
    border: 2px solid gray;
    padding: 10px
""")

layout.addWidget(display)

# -------------------------
# Button Grid
# -------------------------

grid = QGridLayout()
layout.addLayout(grid)

# <- Add the button here 

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

    button.clicked.connect(lambda checked=False, t=text:  button_clicked(t))
    
    row = index //4
    column = index % 4

    grid.addWidget(button, row, column)

window.show()

app.exec()