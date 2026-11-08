"""Qt interface for the multi-base integer Programmer mode."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ...core.errors import CalculatorError
from ...modes.programmer import NumberBase, ProgrammerCalculator, Signedness, WordSize


class ProgrammerPage(QWidget):
    """Programmer mode interface with multi-base readouts and bitwise controls."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.input_is_error = False
        self.base_selector = QComboBox()
        self.word_size_selector = QComboBox()
        self.signedness_selector = QComboBox()
        self.input = QLineEdit("0")
        self.status = QLabel()
        self.value_labels: dict[NumberBase, QLabel] = {}
        self.bits = QLabel("0000 0000 0000 0000 0000 0000 0000 0000")
        self.keypad_buttons: dict[str, list[QPushButton]] = {}

        self._create_ui()
        self._connect_signals()
        self.refresh()

    def _create_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Configuration selectors
        selectors = QHBoxLayout()
        selectors.setSpacing(8)

        # Base selector
        base_label = QLabel("Base:")
        selectors.addWidget(base_label)
        self.base_selector.setObjectName("programmerBase")
        self.base_selector.addItems([b.value for b in NumberBase])
        self.base_selector.setCurrentText(NumberBase.DEC.value)
        selectors.addWidget(self.base_selector)

        # Word size selector
        word_label = QLabel("Word:")
        selectors.addWidget(word_label)
        self.word_size_selector.setObjectName("wordSize")
        self.word_size_selector.addItems(["8-bit", "16-bit", "32-bit", "64-bit"])
        self.word_size_selector.setCurrentText("32-bit")
        selectors.addWidget(self.word_size_selector)

        # Signedness
        sign_label = QLabel("Sign:")
        selectors.addWidget(sign_label)
        self.signedness_selector.setObjectName("signedness")
        self.signedness_selector.addItems(["UNSIGNED", "SIGNED"])
        self.signedness_selector.setCurrentText("UNSIGNED")
        selectors.addWidget(self.signedness_selector)

        selectors.addStretch()
        layout.addLayout(selectors)

        # Expression / Input field
        self.input.setObjectName("programmerInput")
        self.input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.input.setMinimumHeight(44)
        layout.addWidget(self.input)

        # Multi-base readouts
        conversion_grid = QGridLayout()
        conversion_grid.setHorizontalSpacing(10)
        conversion_grid.setVerticalSpacing(2)

        for row, base in enumerate(NumberBase):
            lbl_tag = QLabel(f"<b>{base.value}</b>")
            lbl_tag.setFixedWidth(40)
            conversion_grid.addWidget(lbl_tag, row, 0)

            val_label = QLabel("0")
            val_label.setObjectName("programmerRadixValue")
            val_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            val_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            val_label.setToolTip(f"Double-click to copy {base.value} value")
            self.value_labels[base] = val_label
            conversion_grid.addWidget(val_label, row, 1)

        layout.addLayout(conversion_grid)

        # Bit pattern display
        bit_title = QLabel("Bit Representation (MSB → LSB):")
        layout.addWidget(bit_title)

        self.bits.setObjectName("programmerBits")
        self.bits.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bits.setWordWrap(True)
        self.bits.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.bits)

        # Keypad
        self._create_keypad(layout)

        # Status
        self.status.setObjectName("displayStatus")
        layout.addWidget(self.status)

    def _create_keypad(self, parent: QVBoxLayout) -> None:
        keypad = QGridLayout()
        keypad.setSpacing(6)

        buttons = [
            ("AND", 0, 0, "operatorButton"),
            ("OR", 0, 1, "operatorButton"),
            ("XOR", 0, 2, "operatorButton"),
            ("NOT", 0, 3, "operatorButton"),
            ("<<", 0, 4, "operatorButton"),
            (">>", 0, 5, "operatorButton"),
            ("(", 1, 0, "operatorButton"),
            (")", 1, 1, "operatorButton"),
            ("AC", 1, 2, "clearButton"),
            ("⌫", 1, 3, "backspaceButton"),
            ("=", 1, 4, "equalsButton"),
            ("+", 1, 5, "operatorButton"),
            ("7", 2, 0, "numberButton"),
            ("8", 2, 1, "numberButton"),
            ("9", 2, 2, "numberButton"),
            ("-", 2, 3, "operatorButton"),
            ("A", 2, 4, "numberButton"),
            ("B", 2, 5, "numberButton"),
            ("4", 3, 0, "numberButton"),
            ("5", 3, 1, "numberButton"),
            ("6", 3, 2, "numberButton"),
            ("*", 3, 3, "operatorButton"),
            ("C", 3, 4, "numberButton"),
            ("D", 3, 5, "numberButton"),
            ("1", 4, 0, "numberButton"),
            ("2", 4, 1, "numberButton"),
            ("3", 4, 2, "numberButton"),
            ("/", 4, 3, "operatorButton"),
            ("E", 4, 4, "numberButton"),
            ("F", 4, 5, "numberButton"),
            ("0", 5, 0, "numberButton"),
        ]

        for text, row, col, obj_name in buttons:
            btn = QPushButton(text)
            btn.setObjectName(obj_name)
            btn.clicked.connect(lambda checked=False, val=text: self.button_clicked(val))
            if text == "0":
                keypad.addWidget(btn, row, col, 1, 6)
            else:
                keypad.addWidget(btn, row, col)
            self.keypad_buttons.setdefault(text, []).append(btn)

        parent.addLayout(keypad)

    def _connect_signals(self) -> None:
        self.input.textChanged.connect(self.refresh)
        self.base_selector.currentTextChanged.connect(self.refresh)
        self.word_size_selector.currentTextChanged.connect(self.refresh)
        self.signedness_selector.currentTextChanged.connect(self.refresh)

    @property
    def calculator(self) -> ProgrammerCalculator:
        word_size_int = int(self.word_size_selector.currentText().split("-")[0])
        return ProgrammerCalculator(
            base=NumberBase(self.base_selector.currentText()),
            word_size=WordSize(word_size_int),
            signed=Signedness(self.signedness_selector.currentText()),
        )

    def button_clicked(self, text: str) -> None:
        if text == "AC":
            self.input_is_error = False
            self.input.setText("0")
        elif text == "⌫":
            self.backspace()
        elif text == "=":
            self.calculate()
        elif text == "NOT":
            curr = self.input.text()
            self.input.setText(f"NOT ({curr})")
        elif text in ("AND", "OR", "XOR", "<<", ">>", "+", "-", "*", "/"):
            self.append_text(f" {text} ")
        else:
            self.append_text(text)

    def append_text(self, text: str) -> None:
        if self.input_is_error:
            self.input_is_error = False
            self.input.setText("")
        current = self.input.text()
        if current == "0" and text.strip() not in ("+", "-"):
            self.input.setText(text)
        else:
            self.input.setText(current + text)

    def backspace(self) -> None:
        if self.input_is_error or len(self.input.text()) <= 1:
            self.input_is_error = False
            self.input.setText("0")
        else:
            self.input.setText(self.input.text()[:-1])

    def calculate(self) -> None:
        try:
            result = self.calculator.evaluate_raw(self.input.text())
            self.input_is_error = False
            self.input.setText(self.calculator.format_value(result))
            self.status.clear()
        except CalculatorError as err:
            self.input_is_error = True
            self.status.setText(err.message)

    def refresh(self) -> None:
        try:
            calc = self.calculator
            raw = calc.evaluate_raw(self.input.text())
            for base, label in self.value_labels.items():
                label.setText(calc.format_value(raw, base))

            # Format bits with grouping for readability
            bit_str = calc.bit_string(raw)
            grouped_bits = " ".join(bit_str[i : i + 4] for i in range(0, len(bit_str), 4))
            self.bits.setText(grouped_bits)
            self.status.clear()
            self.input_is_error = False
        except CalculatorError as err:
            for label in self.value_labels.values():
                label.setText("—")
            self.bits.setText("—")
            self.status.setText(err.message)

        self._update_digit_buttons()

    def _update_digit_buttons(self) -> None:
        active_base = NumberBase(self.base_selector.currentText())
        valid_digits = {
            NumberBase.BIN: set("01"),
            NumberBase.OCT: set("01234567"),
            NumberBase.DEC: set("0123456789"),
            NumberBase.HEX: set("0123456789ABCDEF"),
        }[active_base]

        for digit, buttons in self.keypad_buttons.items():
            if len(digit) == 1 and digit.isalnum():
                for btn in buttons:
                    btn.setEnabled(digit.upper() in valid_digits)
