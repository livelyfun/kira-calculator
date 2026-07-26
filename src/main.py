import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget,
)

app = QApplication(sys.argv)

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

layout.addWidget(display)
window.show()

app.exec()