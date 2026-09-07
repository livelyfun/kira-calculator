"""Main application window for Kira Calculator."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QKeyEvent
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from kira_calculator.core import HistoryManager, calculate
from kira_calculator.ui.pages import CalculatorPage, ConverterPage, ProgrammerPage
from kira_calculator.ui.widgets.mode_bar import ModeBar


class CalculatorWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Kira Calculator")
        self.resize(860, 720)
        self.setMinimumSize(720, 580)
        # No hard maximum – allow larger screens

        # Optional persistent history
        history_path = Path.home() / ".kira_calculator" / "history.json"
        self.history_manager = HistoryManager(persist_path=history_path)

        self.just_calculated = False
        self._build_ui()
        self._connect_signals()
        self._load_history()

        # Try to set window icon
        icon_path = Path(__file__).resolve().parents[2] / "resources" / "icon.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

    # ------------------------------------------------------------------ UI
    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(16, 16, 16, 16)

        # Left: calculator area
        left = QVBoxLayout()
        left.setSpacing(12)

        self.display = QLabel("0")
        self.display.setObjectName("display")
        self.display.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.display.setMinimumHeight(90)
        self.display.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        left.addWidget(self.display)

        self.mode_bar = ModeBar()
        left.addWidget(self.mode_bar)

        self.stack = QStackedWidget()
        self.calculator_page = CalculatorPage()
        self.programmer_page = ProgrammerPage()
        self.converter_page = ConverterPage()

        self.stack.addWidget(self.calculator_page)
        self.stack.addWidget(self.programmer_page)
        self.stack.addWidget(self.converter_page)
        left.addWidget(self.stack)

        left_widget = QWidget()
        left_widget.setLayout(left)
        left_widget.setMinimumWidth(480)
        main_layout.addWidget(left_widget, 5)

        # Right: history
        right = QVBoxLayout()
        right.setSpacing(10)

        title = QLabel("History")
        title.setObjectName("historyTitle")
        right.addWidget(title)

        self.history_list = QListWidget()
        self.history_list.setObjectName("history")
        right.addWidget(self.history_list)

        clear_btn = QPushButton("Clear History")
        clear_btn.setObjectName("clearHistoryButton")
        clear_btn.clicked.connect(self._clear_history)
        right.addWidget(clear_btn)

        right_widget = QWidget()
        right_widget.setLayout(right)
        right_widget.setMinimumWidth(220)
        main_layout.addWidget(right_widget, 2)

    def _connect_signals(self) -> None:
        # Mode switching (exclusive via QButtonGroup)
        self.mode_bar.group.idClicked.connect(self.stack.setCurrentIndex)

        # Calculator buttons
        scientific = {
            "sin", "cos", "tan", "log", "ln", "√", "π", "e",
            "x²", "xʸ", "%", "±", "1/x", "(", ")",
        }
        for text, btn in self.calculator_page.buttons.items():
            if text in scientific:
                btn.clicked.connect(
                    lambda checked=False, t=text: self._scientific_clicked(t)
                )
            else:
                btn.clicked.connect(
                    lambda checked=False, t=text: self._button_clicked(t)
                )

        self.history_list.itemDoubleClicked.connect(self._restore_history)

    def _load_history(self) -> None:
        for entry in self.history_manager.entries():
            self.history_list.addItem(entry)

    # ----------------------------------------------------------- Key events
    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()
        text = event.text()

        if text.isdigit() or text in "+-.":
            self._append_text(text)
        elif text == "*":
            self._append_text("×")
        elif text == "/":
            self._append_text("÷")
        elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._calculate()
        elif key == Qt.Key.Key_Backspace:
            self._backspace()
        elif key == Qt.Key.Key_Escape:
            self._clear()
        else:
            super().keyPressEvent(event)

    # -------------------------------------------------------- Button logic
    def _button_clicked(self, text: str) -> None:
        if text == "C":
            self._clear()
        elif text == "=":
            self._calculate()
        elif text == "⌫":
            self._backspace()
        else:
            self._append_text(text)

    def _scientific_clicked(self, text: str) -> None:
        mapping = {
            "sin": "sin(",
            "cos": "cos(",
            "tan": "tan(",
            "log": "log10(",
            "ln": "ln(",
            "√": "sqrt(",
            "π": "pi",
            "e": "e",
            "x²": "**2",
            "xʸ": "**",
            "1/x": "1/(",
            "%": "/100",
        }
        if text == "±":
            current = self.display.text()
            if current.startswith("-"):
                self.display.setText(current[1:])
            else:
                if current != "0":
                    self.display.setText("-" + current)
            return
        self._append_text(mapping.get(text, text))

    def _append_text(self, text: str) -> None:
        current = self.display.text()
        operators = {"+", "-", "×", "÷"}

        if self.just_calculated:
            # After =, start fresh unless the new token is an operator
            if text in operators:
                self.just_calculated = False
                # keep current result and append operator
            else:
                self.display.setText(text)
                self.just_calculated = False
                return

        if current == "0" and text in {"×", "÷"}:
            return

        if current and current[-1] in operators and text in operators:
            self.display.setText(current[:-1] + text)
            return

        if text == ".":
            last = current
            for op in operators:
                last = last.split(op)[-1]
            if "." in last:
                return

        if current == "0" and text not in operators and text != ".":
            self.display.setText(text)
        else:
            self.display.setText(current + text)

    def _clear(self) -> None:
        self.display.setText("0")
        self.just_calculated = False

    def _backspace(self) -> None:
        current = self.display.text()
        if current in {"Error", "0"} or len(current) == 1:
            self.display.setText("0")
            return
        self.display.setText(current[:-1])

    def _calculate(self) -> None:
        expression = self.display.text()
        result = calculate(expression)

        if result != "Error":
            self.history_manager.add(expression, result)
            self.history_list.insertItem(0, f"{expression} = {result}")
            self.just_calculated = True

        self.display.setText(result)

    def _restore_history(self, item) -> None:
        text = item.text()
        expression = text.split("=")[0].strip()
        self.display.setText(expression)
        self.just_calculated = False

    def _clear_history(self) -> None:
        self.history_manager.clear()
        self.history_list.clear()
