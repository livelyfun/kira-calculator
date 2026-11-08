"""Theme loader for Kira Calculator."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

THEMES_DIR = Path(__file__).parent


def load_theme(name: str = "dark") -> str:
    """Load QSS stylesheet by name ('dark', 'light', or 'system')."""
    normalized = name.lower()
    if "system" in normalized:
        app = QApplication.instance()
        if app and hasattr(app, "styleHints"):
            try:
                scheme = app.styleHints().colorScheme()
                normalized = "light" if scheme == Qt.ColorScheme.Light else "dark"
            except Exception:
                normalized = "dark"
        else:
            normalized = "dark"

    if normalized in ("light", "white"):
        qss_file = THEMES_DIR / "light.qss"
    else:
        # Default to dark theme
        qss_file = THEMES_DIR / "dark.qss"

    if qss_file.exists():
        return qss_file.read_text(encoding="utf-8")
    return ""


def apply_theme(app: QApplication, name: str = "dark") -> None:
    """Apply the requested theme stylesheet to the active QApplication instance."""
    qss = load_theme(name)
    app.setStyleSheet(qss)
