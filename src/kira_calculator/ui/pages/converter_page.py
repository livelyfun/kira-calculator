"""Interactive Unit Converter UI with real-time bidirectional conversion."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ...core.formatter import format_number
from ...modes.converter import UnitConverter


class ConverterPage(QWidget):
    """Practical unit conversion interface across 8 physical and digital domains."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._updating = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # 1. Category selector
        cat_box = QHBoxLayout()
        cat_label = QLabel("Category:")
        cat_box.addWidget(cat_label)

        self.category_combo = QComboBox()
        self.category_combo.setObjectName("categoryCombo")
        self.category_combo.addItems(UnitConverter.get_categories())
        self.category_combo.currentTextChanged.connect(self._on_category_changed)
        cat_box.addWidget(self.category_combo)
        cat_box.addStretch()
        layout.addLayout(cat_box)

        # 2. Main Conversion Cards Frame
        card_frame = QFrame()
        card_frame.setObjectName("displayFrame")
        card_layout = QVBoxLayout(card_frame)
        card_layout.setSpacing(12)

        # From Row
        from_header = QLabel("From:")
        card_layout.addWidget(from_header)

        from_row = QHBoxLayout()
        self.from_input = QLineEdit("1")
        self.from_input.setObjectName("converterInput")
        self.from_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.from_input.textChanged.connect(self._on_from_text_changed)
        from_row.addWidget(self.from_input, 2)

        self.from_unit_combo = QComboBox()
        self.from_unit_combo.setObjectName("fromUnitCombo")
        self.from_unit_combo.currentTextChanged.connect(self._on_unit_changed)
        from_row.addWidget(self.from_unit_combo, 3)
        card_layout.addLayout(from_row)

        # Swap button row
        swap_row = QHBoxLayout()
        swap_row.addStretch()
        self.swap_btn = QPushButton("⇅ Swap Units")
        self.swap_btn.setObjectName("navButton")
        self.swap_btn.clicked.connect(self._on_swap_clicked)
        swap_row.addWidget(self.swap_btn)
        swap_row.addStretch()
        card_layout.addLayout(swap_row)

        # To Row
        to_header = QLabel("To:")
        card_layout.addWidget(to_header)

        to_row = QHBoxLayout()
        self.to_input = QLineEdit("0")
        self.to_input.setObjectName("converterInput")
        self.to_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.to_input.textChanged.connect(self._on_to_text_changed)
        to_row.addWidget(self.to_input, 2)

        self.to_unit_combo = QComboBox()
        self.to_unit_combo.setObjectName("toUnitCombo")
        self.to_unit_combo.currentTextChanged.connect(self._on_unit_changed)
        to_row.addWidget(self.to_unit_combo, 3)
        card_layout.addLayout(to_row)

        # Rate summary label
        self.rate_label = QLabel("")
        self.rate_label.setObjectName("displayStatus")
        self.rate_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.rate_label)

        layout.addWidget(card_frame)
        layout.addStretch()

        # Initialize with default category
        self._populate_units_for_category(self.category_combo.currentText())

    def _on_category_changed(self, category: str) -> None:
        self._populate_units_for_category(category)

    def _populate_units_for_category(self, category: str) -> None:
        units = UnitConverter.get_units(category)
        self._updating = True
        self.from_unit_combo.clear()
        self.to_unit_combo.clear()
        self.from_unit_combo.addItems(units)
        self.to_unit_combo.addItems(units)

        if len(units) > 1:
            self.to_unit_combo.setCurrentIndex(1)
        self._updating = False
        self._convert_forward()

    def _on_unit_changed(self) -> None:
        if not self._updating:
            self._convert_forward()

    def _on_swap_clicked(self) -> None:
        from_idx = self.from_unit_combo.currentIndex()
        to_idx = self.to_unit_combo.currentIndex()
        self._updating = True
        self.from_unit_combo.setCurrentIndex(to_idx)
        self.to_unit_combo.setCurrentIndex(from_idx)
        self._updating = False
        self._convert_forward()

    def _on_from_text_changed(self, text: str) -> None:
        if self._updating:
            return
        self._convert_forward()

    def _on_to_text_changed(self, text: str) -> None:
        if self._updating:
            return
        self._convert_backward()

    def _convert_forward(self) -> None:
        from_text = self.from_input.text().strip()
        from_unit = self.from_unit_combo.currentText()
        to_unit = self.to_unit_combo.currentText()
        cat = self.category_combo.currentText()

        if not from_text or not from_unit or not to_unit:
            return

        try:
            val = float(from_text)
            res = UnitConverter.convert(val, from_unit, to_unit, cat)
            self._updating = True
            self.to_input.setText(format_number(res))
            self._updating = False

            # Update formula preview
            sample = UnitConverter.convert(1.0, from_unit, to_unit, cat)
            self.rate_label.setText(f"1 {from_unit} = {format_number(sample)} {to_unit}")
        except ValueError:
            self.rate_label.setText("Invalid numerical input")

    def _convert_backward(self) -> None:
        to_text = self.to_input.text().strip()
        from_unit = self.from_unit_combo.currentText()
        to_unit = self.to_unit_combo.currentText()
        cat = self.category_combo.currentText()

        if not to_text or not from_unit or not to_unit:
            return

        try:
            val = float(to_text)
            res = UnitConverter.convert(val, to_unit, from_unit, cat)
            self._updating = True
            self.from_input.setText(format_number(res))
            self._updating = False
        except ValueError:
            self.rate_label.setText("Invalid numerical input")

