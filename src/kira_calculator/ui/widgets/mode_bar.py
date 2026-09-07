"""Exclusive mode switcher (Calculator / Programmer / Converter)."""

from __future__ import annotations

from PySide6.QtWidgets import QButtonGroup, QHBoxLayout, QPushButton, QWidget


class ModeBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.calculator_button = QPushButton("Calculator")
        self.programmer_button = QPushButton("Programmer")
        self.converter_button = QPushButton("Converter")

        self.group = QButtonGroup(self)
        self.group.setExclusive(True)

        for i, btn in enumerate(
            (self.calculator_button, self.programmer_button, self.converter_button)
        ):
            btn.setCheckable(True)
            btn.setObjectName("modeButton")
            self.group.addButton(btn, i)
            layout.addWidget(btn)

        self.calculator_button.setChecked(True)
