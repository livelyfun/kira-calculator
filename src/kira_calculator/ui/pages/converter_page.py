"""Unit converter mode (scaffold)."""

from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class ConverterPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        label = QLabel(
            "Unit Converter\n\n"
            "Length • Mass • Temperature • Data\n"
            "Coming in the next iteration"
        )
        label.setObjectName("placeholderLabel")
        label.setStyleSheet("color: #aaaaaa; font-size: 22px;")
        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()
