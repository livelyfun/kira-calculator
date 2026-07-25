import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Kira Calculator")
window.resize(400, 600)


window.show()

app.exec()