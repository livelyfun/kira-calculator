import sys
from pathlib import Path

# Ensure the project package is importable when running main.py directly.
src_dir = Path(__file__).resolve().parent
project_root = src_dir.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication  # noqa: E402

from src.ui.window import CalculatorWindow  # noqa: E402


def main() -> None:
    app = QApplication(sys.argv)

    style_path = Path(__file__).parent / "styles" / "main.qss"

    if style_path.exists():
        app.setStyleSheet(style_path.read_text(encoding="utf-8"))

    window = CalculatorWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
