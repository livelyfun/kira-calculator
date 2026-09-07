"""Programmer mode – hex / binary / octal / bitwise (scaffold)."""

from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class ProgrammerPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        label = QLabel(
            "Programmer Mode\n\n"
            "Hex • Binary • Octal • Bitwise\n"
            "Coming in the next iteration"
        )
        label.setObjectName("placeholderLabel")
        label.setStyleSheet("color: #aaaaaa; font-size: 22px;")
        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()
