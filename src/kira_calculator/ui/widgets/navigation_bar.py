"""Navigation bar coordinating calculator mode switching, theme selection, and history drawer."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QPushButton,
)


class NavigationBar(QFrame):
    """Top-level modern navigation bar."""

    mode_changed = Signal(str)
    theme_changed = Signal(str)
    history_toggled = Signal()

    MODES = ["Standard", "Scientific", "Programmer", "Converter"]

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("navigationBar")
        self.mode_buttons: dict[str, QPushButton] = {}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(6)

        # Mode buttons
        for mode in self.MODES:
            btn = QPushButton(mode)
            btn.setObjectName("navButton")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked=False, m=mode: self._on_mode_clicked(m))
            layout.addWidget(btn)
            self.mode_buttons[mode] = btn

        layout.addStretch()

        # Theme selector dropdown
        self.theme_combo = QComboBox()
        self.theme_combo.setObjectName("themeCombo")
        self.theme_combo.addItems(["Dark Theme", "Light Theme", "System Theme"])
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        layout.addWidget(self.theme_combo)

        # History button
        self.history_btn = QPushButton("🕒 History")
        self.history_btn.setObjectName("navButton")
        self.history_btn.setCheckable(True)
        self.history_btn.clicked.connect(self.history_toggled.emit)
        layout.addWidget(self.history_btn)

        self.set_active_mode("Standard")

    def _on_mode_clicked(self, mode: str) -> None:
        self.set_active_mode(mode)
        self.mode_changed.emit(mode)

    def set_active_mode(self, active_mode: str) -> None:
        for mode, btn in self.mode_buttons.items():
            btn.setChecked(mode == active_mode)
            btn.setProperty("active", "true" if mode == active_mode else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def _on_theme_changed(self, text: str) -> None:
        if "system" in text.lower():
            mode_key = "system"
        elif "light" in text.lower():
            mode_key = "light"
        else:
            mode_key = "dark"
        self.theme_changed.emit(mode_key)

    def set_theme_choice(self, theme_name: str) -> None:
        if "system" in theme_name.lower():
            self.theme_combo.setCurrentText("System Theme")
        elif "light" in theme_name.lower():
            self.theme_combo.setCurrentText("Light Theme")
        else:
            self.theme_combo.setCurrentText("Dark Theme")
