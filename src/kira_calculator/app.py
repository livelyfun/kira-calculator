"""Application bootstrap for Kira Calculator."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from kira_calculator.ui import CalculatorWindow


def _load_stylesheet(app: QApplication) -> None:
    theme_path = Path(__file__).parent / "ui" / "themes" / "dark.qss"
    if theme_path.exists():
        app.setStyleSheet(theme_path.read_text(encoding="utf-8"))


def run() -> int:
    # High-DPI support
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("Kira Calculator")
    app.setOrganizationName("livelyfun")
    app.setApplicationVersion("1.0.0")

    # Prefer a clean system font
    font = QFont("Segoe UI", 10)
    if sys.platform == "darwin":
        font = QFont("SF Pro Text", 13)
    elif sys.platform.startswith("linux"):
        font = QFont("Ubuntu", 10)
    app.setFont(font)

    _load_stylesheet(app)

    window = CalculatorWindow()
    window.show()

    return app.exec()


def main() -> None:
    sys.exit(run())
