"""Application entry point and Qt lifecycle management."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from .services.history_service import HistoryService
from .services.settings_service import SettingsService
from .ui.main_window import MainWindow
from .ui.themes import apply_theme

APP_NAME = "Kira Calculator"
APP_VERSION = "1.0.0"
ORG_NAME = "KiraCalculator"


def create_application() -> tuple[QApplication, MainWindow]:
    """Create and configure the QApplication and MainWindow instances."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName(ORG_NAME)

    settings_service = SettingsService()
    history_service = HistoryService()

    # Apply saved theme
    apply_theme(app, settings_service.settings.theme)

    window = MainWindow(
        history_service=history_service,
        settings_service=settings_service,
    )
    return app, window


def main() -> int:
    """Standard CLI / desktop entry point."""
    app, window = create_application()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
