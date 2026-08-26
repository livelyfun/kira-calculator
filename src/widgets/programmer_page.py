"""Qt interface for the integer Programmer mode."""

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

try:
    from calculator.errors import CalculatorError
    from calculator.programmer import NumberBase, ProgrammerCalculator, Signedness
except ImportError:
    from src.calculator.errors import CalculatorError
    from src.calculator.programmer import NumberBase, ProgrammerCalculator, Signedness


class ProgrammerPage(QWidget):
    """Programmer calculator controls and base/bit representations."""

    def __init__(self) -> None:
        super().__init__()
        self.input_is_error = False
        self.base_selector = QComboBox()
        self.word_size_selector = QComboBox()
        self.signedness_selector = QComboBox()
        self.input = QLineEdit("0")
        self.status = QLabel()
        self.value_labels: dict[NumberBase, QLabel] = {}
        self.bits = QLabel("00000000000000000000000000000000")

        self._create_ui()
        self._connect_signals()
        self.refresh()

    def _create_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        selectors = QHBoxLayout()
        for selector, values, name in (
            (self.base_selector, [base.value for base in NumberBase], "programmerBase"),
            (
                self.word_size_selector,
                ["8-bit", "16-bit", "32-bit", "64-bit"],
                "wordSize",
            ),
            (self.signedness_selector, ["UNSIGNED", "SIGNED"], "signedness"),
        ):
            selector.addItems(values)
            selector.setObjectName(name)
            selectors.addWidget(selector)
        self.word_size_selector.setCurrentText("32-bit")
        self.base_selector.setCurrentText(NumberBase.DEC.value)
        layout.addLayout(selectors)

        self.input.setObjectName("programmerInput")
        self.input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.input.setMinimumHeight(54)
        layout.addWidget(self.input)

        conversion_grid = QGridLayout()
        conversion_grid.setHorizontalSpacing(12)
        conversion_grid.setVerticalSpacing(4)
        for row, base in enumerate(NumberBase):
            conversion_grid.addWidget(QLabel(f"{base.value}:"), row, 0)
            label = QLabel("—")
            label.setObjectName(f"programmer{base.value}")
            label.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.value_labels[base] = label
            conversion_grid.addWidget(label, row, 1)
        layout.addLayout(conversion_grid)

        bit_title = QLabel("Bits (most significant → least significant)")
        bit_title.setObjectName("programmerBitTitle")
        layout.addWidget(bit_title)
        self.bits.setObjectName("programmerBits")
        self.bits.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bits.setWordWrap(True)
        layout.addWidget(self.bits)

        self._create_keypad(layout)
        self.status.setObjectName("programmerStatus")
        layout.addWidget(self.status)

    def _create_keypad(self, parent: QVBoxLayout) -> None:
        keypad = QGridLayout()
        keypad.setSpacing(6)
        buttons = [
            ("AND", 0, 0),
            ("OR", 0, 1),
            ("XOR", 0, 2),
            ("NOT", 0, 3),
            ("<<", 0, 4),
            (">>", 0, 5),
            ("(", 1, 0),
            (")", 1, 1),
            ("AC", 1, 2),
            ("⌫", 1, 3),
            ("=", 1, 4),
            ("+", 1, 5),
            ("7", 2, 0),
            ("8", 2, 1),
            ("9", 2, 2),
            ("-", 2, 3),
            ("A", 2, 4),
            ("B", 2, 5),
            ("4", 3, 0),
            ("5", 3, 1),
            ("6", 3, 2),
            ("*", 3, 3),
            ("C", 3, 4),
            ("D", 3, 5),
            ("1", 4, 0),
            ("2", 4, 1),
            ("3", 4, 2),
            ("/", 4, 3),
            ("E", 4, 4),
            ("F", 4, 5),
            ("0", 5, 0),
        ]
        self.keypad_buttons: dict[str, list[QPushButton]] = {}
        for text, row, column in buttons:
            button = QPushButton(text)
            button.setObjectName("programmerButton")
            button.clicked.connect(
                lambda checked=False, value=text: self.button_clicked(value)
            )
            keypad.addWidget(button, row, column)
            self.keypad_buttons.setdefault(text, []).append(button)
        parent.addLayout(keypad)

    def _connect_signals(self) -> None:
        self.input.textChanged.connect(self.refresh)
        self.base_selector.currentTextChanged.connect(self.refresh)
        self.word_size_selector.currentTextChanged.connect(self.refresh)
        self.signedness_selector.currentTextChanged.connect(self.refresh)

    @property
    def calculator(self) -> ProgrammerCalculator:
        return ProgrammerCalculator(
            base=NumberBase(self.base_selector.currentText()),
            word_size=int(self.word_size_selector.currentText().split("-")[0]),
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
        elif text in ("NOT",):
            current = self.input.text()
            self.input.setText(f"NOT ({current})")
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
        except CalculatorError as error:
            self.input_is_error = True
            self.status.setText(error.message)

    def refresh(self) -> None:
        try:
            calculator = self.calculator
            raw = calculator.evaluate_raw(self.input.text())
            for base, label in self.value_labels.items():
                label.setText(calculator.format_value(raw, base))
            self.bits.setText(calculator.bit_string(raw))
            self.status.clear()
            self.input_is_error = False
        except CalculatorError as error:
            for label in self.value_labels.values():
                label.setText("—")
            self.bits.setText("—")
            self.status.setText(error.message)

        self._update_digit_buttons()

    def _update_digit_buttons(self) -> None:
        valid = {
            NumberBase.BIN: set("01"),
            NumberBase.OCT: set("01234567"),
            NumberBase.DEC: set("0123456789"),
            NumberBase.HEX: set("0123456789ABCDEF"),
        }[NumberBase(self.base_selector.currentText())]
        for digit, buttons in self.keypad_buttons.items():
            if len(digit) == 1 and digit.isalnum():
                for button in buttons:
                    button.setEnabled(digit in valid)
