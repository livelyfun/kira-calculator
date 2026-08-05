import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from ui.window import CalculatorWindow


def main():

    app = QApplication(sys.argv)

    style_path = Path(__file__).parent / "styles" / "main.qss"

    if style_path.exists():
        with open(style_path, "r") as file:
            app.setStyleSheet(file.read())

    window = CalculatorWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()