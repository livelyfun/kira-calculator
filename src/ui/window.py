from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
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

try:
    from calculator.logic import evaluate_expression
    from widgets.calculator_page import CalculatorPage
    from widgets.converter_page import ConverterPage
    from widgets.mode_bar import ModeBar
    from widgets.programmer_page import ProgrammerPage
except ImportError:
    from src.calculator.logic import evaluate_expression
    from src.widgets.calculator_page import CalculatorPage
    from src.widgets.converter_page import ConverterPage
    from src.widgets.mode_bar import ModeBar
    from src.widgets.programmer_page import ProgrammerPage


class CalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kira Calculator")
        self.resize(820, 700)
        self.setMinimumSize(800, 620)
        self.setMaximumSize(900, 800)

        self.angle_mode = "DEG"

        self.create_ui()

        self.just_calculated = False

    def create_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(15, 15, 15, 15)

        central_widget.setLayout(self.main_layout)

        # ==========================
        # Left Side (Calculator)
        # ==========================

        self.calculator_layout = QVBoxLayout()
        self.calculator_layout.setSpacing(15)

        self.create_display()
        self.mode_bar = ModeBar()
        self.calculator_layout.addWidget(self.mode_bar)
        self.stack = QStackedWidget()

        self.calculator_page = CalculatorPage()
        self.calculator_page.angle_selector.currentTextChanged.connect(
            self.angle_mode_changed
        )
        for text, button in self.calculator_page.buttons.items():
            if text in [
                "sin",
                "cos",
                "tan",
                "log",
                "ln",
                "√",
                "π",
                "e",
                "x²",
                "xʸ",
                "%",
                "±",
                "1/x",
                "(",
                ")",
            ]:
                button.clicked.connect(
                    lambda checked=False, t=text: self.scientific_button_clicked(t)
                )

            else:
                button.clicked.connect(
                    lambda checked=False, t=text: self.button_clicked(t)
                )
        self.programmer_page = ProgrammerPage()
        self.converter_page = ConverterPage()

        self.stack.addWidget(self.calculator_page)

        self.stack.addWidget(self.programmer_page)
        self.stack.addWidget(self.converter_page)

        self.calculator_layout.addWidget(self.stack)

        self.mode_bar.calculator_button.clicked.connect(
            lambda: self.stack.setCurrentIndex(0)
        )

        self.mode_bar.programmer_button.clicked.connect(
            lambda: self.stack.setCurrentIndex(1)
        )

        self.mode_bar.converter_button.clicked.connect(
            lambda: self.stack.setCurrentIndex(2)
        )

        calculator_widget = QWidget()
        calculator_widget.setLayout(self.calculator_layout)
        calculator_widget.setMinimumWidth(500)

        self.main_layout.addWidget(calculator_widget, 5)

        # ==========================
        # Right Side (History)
        # ==========================

        self.history_layout = QVBoxLayout()
        self.history_layout.setSpacing(10)

        self.create_history()

        history_widget = QWidget()
        history_widget.setLayout(self.history_layout)
        history_widget.setMinimumWidth(240)

        self.main_layout.addWidget(history_widget, 2)

    def create_display(self):

        self.display = QLabel("0")

        self.display.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        self.display.setMinimumHeight(100)

        self.display.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.calculator_layout.addWidget(self.display)

    def create_history(self):

        title = QLabel("History")
        title.setObjectName("historyTitle")

        self.history = QListWidget()
        self.history.setObjectName("history")

        self.history.itemDoubleClicked.connect(self.restore_history)

        clear_button = QPushButton("Clear History")
        clear_button.setObjectName("clearHistoryButton")
        clear_button.clicked.connect(self.history.clear)

        self.history_layout.addWidget(title)
        self.history_layout.addWidget(self.history)
        self.history_layout.addWidget(clear_button)

    def keyPressEvent(self, event: QKeyEvent):

        key = event.key()
        text = event.text()

        if text.isdigit() or text in ["+", "-", "."]:
            self.append_text(text)

        elif text == "*":
            self.append_text("×")

        elif text == "/":
            self.append_text("÷")

        elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.calculate_result()

        elif key == Qt.Key.Key_Backspace:
            self.backspace()

        elif key == Qt.Key.Key_Escape:
            self.clear_display()

        else:
            super().keyPressEvent(event)

    def button_clicked(self, text):

        if text == "C":
            self.clear_display()

        elif text == "=":
            self.calculate_result()

        elif text == "⌫":
            self.backspace()

        else:
            self.append_text(text)

    def append_text(self, text):

        current = self.display.text()

        operators = ["+", "-", "×", "÷"]

        # Start fresh after pressing =
        if self.just_calculated:
            self.display.setText(text)
            self.just_calculated = False
            return

        # Prevent starting with × or ÷
        if current == "0" and text in ["×", "÷"]:
            return

        # Replace the last operator if user presses another operator
        if current[-1] in operators and text in operators:
            self.display.setText(current[:-1] + text)
            return
        # Prevent multiple decimal points in the current number
        if text == ".":
            last_number = current

            for operator in ["+", "-", "×", "÷"]:
                last_number = last_number.split(operator)[-1]

            if "." in last_number:
                return
        # Replace the initial 0
        if current == "0":
            self.display.setText(text)
        else:
            self.display.setText(current + text)

    def clear_display(self):

        self.display.setText("0")

    def backspace(self):

        current = self.display.text()

        # If the display currently holds an error message, clear to 0
        if (
            current in ("Error", "NaN", "Infinity", "-Infinity")
            or not current
            or len(current) == 1
            or any(
                err_word in current.lower()
                for err_word in (
                    "error",
                    "invalid",
                    "division",
                    "unexpected",
                    "undefined",
                    "expected",
                )
            )
        ):
            self.display.setText("0")
            return

        self.display.setText(current[:-1])

    def calculate_result(self):
        expression = self.display.text()
        result_obj = evaluate_expression(expression, angle_mode=self.angle_mode)

        if result_obj.success:
            self.history.insertItem(0, f"{expression} = {result_obj.formatted_value}")
            self.display.setText(result_obj.formatted_value)
            self.just_calculated = True
        else:
            self.display.setText(result_obj.formatted_value)
            self.just_calculated = False

    def restore_history(self, item):

        text = item.text()

        expression = text.split("=")[0].strip()

        self.display.setText(expression)

        self.just_calculated = False

    def scientific_button_clicked(self, text):

        if text == "sin":
            self.append_text("sin(")

        elif text == "cos":
            self.append_text("cos(")

        elif text == "tan":
            self.append_text("tan(")

        elif text == "log":
            self.append_text("log(")

        elif text == "ln":
            self.append_text("ln(")

        elif text == "√":
            self.append_text("sqrt(")

        elif text == "π":
            self.append_text("pi")

        elif text == "e":
            self.append_text("e")

        elif text == "x²":
            self.append_text("^2")

        elif text == "xʸ":
            self.append_text("^")

        elif text == "1/x":
            self.append_text("1/(")

        elif text == "%":
            self.append_text("%")

        elif text == "±":
            current = self.display.text()

            if current.startswith("-"):
                self.display.setText(current[1:])
            else:
                self.display.setText("-" + current)

        elif text == "=":
            self.calculate_result()

        else:
            self.append_text(text)

    def angle_mode_changed(self, mode):

        self.angle_mode = mode
