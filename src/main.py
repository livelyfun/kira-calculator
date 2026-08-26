import sys
from pathlib import Path

# Ensure src directory is in sys.path when running main.py directly
src_dir = Path(__file__).resolve().parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from PySide6.QtWidgets import QApplication  # noqa: E402

from ui.window import CalculatorWindow  # noqa: E402


def main():

    app = QApplication(sys.argv)

    style_path = Path(__file__).parent / "styles" / "main.qss"

    if style_path.exists():
        with open(style_path) as file:
            app.setStyleSheet(file.read())

    window = CalculatorWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
