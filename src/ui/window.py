"""Application shell coordinating navigation, pages, and shared expression UI."""

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
    from src.calculator.logic import evaluate_expression
    from src.ui.modes import AppMode
    from src.widgets.calculator_page import CalculatorPage
    from src.widgets.converter_page import ConverterPage
    from src.widgets.mode_bar import ModeBar
    from src.widgets.programmer_page import ProgrammerPage
    from src.widgets.scientific_page import ScientificPage
except ImportError:
    from calculator.logic import evaluate_expression
    from ui.modes import AppMode
    from widgets.calculator_page import CalculatorPage
    from widgets.converter_page import ConverterPage
    from widgets.mode_bar import ModeBar
    from widgets.programmer_page import ProgrammerPage
    from widgets.scientific_page import ScientificPage


class CalculatorWindow(QMainWindow):
    """Coordinate top-level modes and the shared Standard/Scientific state."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Kira Calculator")
        self.resize(820, 700)
        self.setMinimumSize(800, 620)
        self.setMaximumSize(900, 800)

        self.just_calculated = False
        self.display_is_error = False
        self.active_mode = AppMode.STANDARD
        self.pages: dict[AppMode, QWidget] = {}

        self.create_ui()
        self.set_mode(AppMode.STANDARD)

    def create_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(15, 15, 15, 15)

        self.calculator_layout = QVBoxLayout()
        self.calculator_layout.setSpacing(15)

        self.create_display()
        self.mode_bar = ModeBar()
        self.mode_bar.mode_selected.connect(self.set_mode)
        self.calculator_layout.addWidget(self.mode_bar)

        self.stack = QStackedWidget()
        self._create_pages()
        self.calculator_layout.addWidget(self.stack)

        calculator_widget = QWidget()
        calculator_widget.setLayout(self.calculator_layout)
        calculator_widget.setMinimumWidth(500)
        self.main_layout.addWidget(calculator_widget, 5)

        self.history_layout = QVBoxLayout()
        self.history_layout.setSpacing(10)
        self.create_history()

        self.history_widget = QWidget()
        self.history_widget.setLayout(self.history_layout)
        self.history_widget.setMinimumWidth(240)
        self.main_layout.addWidget(self.history_widget, 2)

    def _create_pages(self) -> None:
        self.calculator_page = CalculatorPage()
        self.scientific_page = ScientificPage()
        self.programmer_page = ProgrammerPage()
        self.converter_page = ConverterPage()
        self.pages = {
            AppMode.STANDARD: self.calculator_page,
            AppMode.SCIENTIFIC: self.scientific_page,
            AppMode.PROGRAMMER: self.programmer_page,
            AppMode.CONVERTER: self.converter_page,
        }
        for page in self.pages.values():
            self.stack.addWidget(page)

        self._connect_expression_page(self.calculator_page)
        self._connect_expression_page(self.scientific_page, scientific=True)

    def _connect_expression_page(
        self, page: CalculatorPage, *, scientific: bool = False
    ) -> None:
        handler = self.scientific_button_clicked if scientific else self.button_clicked
        for text, button in page.buttons.items():
            button.clicked.connect(
                lambda checked=False, value=text, click_handler=handler: click_handler(
                    value
                )
            )

    def set_mode(self, mode: AppMode) -> None:
        """Show a page by stable mode identifier rather than a stack index."""
        if not isinstance(mode, AppMode):
            mode = AppMode(mode)
        self.active_mode = mode
        self.stack.setCurrentWidget(self.pages[mode])
        self.mode_bar.set_active_mode(mode)

        uses_expression_model = mode.uses_expression_model
        self.display.setVisible(uses_expression_model)
        self.history_widget.setVisible(uses_expression_model)

    def show_standard_mode(self) -> None:
        self.set_mode(AppMode.STANDARD)

    def show_scientific_mode(self) -> None:
        self.set_mode(AppMode.SCIENTIFIC)

    def show_programmer_mode(self) -> None:
        self.set_mode(AppMode.PROGRAMMER)

    def show_converter_mode(self) -> None:
        self.set_mode(AppMode.CONVERTER)

    def create_display(self) -> None:
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

    def create_history(self) -> None:
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

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Route global expression shortcuts only to expression-based modes."""
        if not self.active_mode.uses_expression_model:
            event.ignore()
            return

        key = event.key()
        text = event.text()
        expression_characters = {"+", "-", ".", "(", ")"}
        if self.active_mode is AppMode.SCIENTIFIC:
            expression_characters.update({"^", "!"})
        if text.isdigit() or text in expression_characters:
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

    def button_clicked(self, text: str) -> None:
        if text == "C":
            self.clear_display()
        elif text == "=":
            self.calculate_result()
        elif text == "⌫":
            self.backspace()
        else:
            self.append_text(text)

    @staticmethod
    def _is_postfix_text(text: str) -> bool:
        """Check whether text should append to the existing expression."""
        return text.startswith("^") or text in {"%", "!"}

    def append_text(self, text: str) -> None:
        if self.display_is_error:
            self.display.setText("0")
            self.display_is_error = False
            self.just_calculated = False

        current = self.display.text()
        operators = ["+", "-", "×", "÷"]
        if self._is_postfix_text(text):
            if self.just_calculated:
                self.just_calculated = False
            self.display.setText(current + text)
            return
        if self.just_calculated:
            self.display.setText(text)
            self.just_calculated = False
            return
        if current == "0" and text in ["×", "÷"]:
            return
        if current[-1] in operators and text in operators:
            self.display.setText(current[:-1] + text)
            return
        if text == ".":
            last_number = current
            for operator in operators:
                last_number = last_number.split(operator)[-1]
            if "." in last_number:
                return
        self.display.setText(text if current == "0" else current + text)

    def clear_display(self) -> None:
        self.display.setText("0")
        self.just_calculated = False
        self.display_is_error = False

    def backspace(self) -> None:
        current = self.display.text()
        if self.display_is_error or not current or len(current) == 1:
            self.display.setText("0")
            self.display_is_error = False
            return
        self.display.setText(current[:-1])

    def calculate_result(self) -> None:
        expression = self.display.text()
        angle_mode = (
            self.scientific_page.angle_selector.currentText()
            if self.active_mode is AppMode.SCIENTIFIC
            else "DEG"
        )
        result_obj = evaluate_expression(expression, angle_mode=angle_mode)
        if result_obj.success:
            self.history.insertItem(0, f"{expression} = {result_obj.formatted_value}")
            self.display.setText(result_obj.formatted_value)
            self.just_calculated = True
            self.display_is_error = False
        else:
            self.display.setText(result_obj.formatted_value)
            self.just_calculated = False
            self.display_is_error = True

    def restore_history(self, item) -> None:
        expression = item.text().split("=")[0].strip()
        self.display.setText(expression)
        self.just_calculated = False
        self.display_is_error = False

    def scientific_button_clicked(self, text: str) -> None:
        scientific_inputs = {
            "sin": "sin(",
            "cos": "cos(",
            "tan": "tan(",
            "asin": "asin(",
            "acos": "acos(",
            "atan": "atan(",
            "sinh": "sinh(",
            "cosh": "cosh(",
            "tanh": "tanh(",
            "log": "log(",
            "ln": "ln(",
            "√": "sqrt(",
            "π": "pi",
            "e": "e",
            "x²": "^2",
            "xʸ": "^",
            "1/x": "1/(",
        }
        if text == "±":
            current = self.display.text()
            self.display.setText(
                current[1:] if current.startswith("-") else "-" + current
            )
        elif text in scientific_inputs:
            self.append_text(scientific_inputs[text])
        else:
            self.button_clicked(text)
