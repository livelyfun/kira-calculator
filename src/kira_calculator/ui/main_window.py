"""Primary application window coordinating navigation, calculation modes, history, and settings."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent, QKeyEvent
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..core.engine import evaluate_expression
from ..services.history_service import HistoryService
from ..services.settings_service import SettingsService
from .pages.converter_page import ConverterPage
from .pages.programmer_page import ProgrammerPage
from .pages.scientific_page import ScientificPage
from .pages.standard_page import StandardPage
from .themes import apply_theme
from .widgets.display import DisplayWidget
from .widgets.history_drawer import HistoryDrawer
from .widgets.navigation_bar import NavigationBar


class MainWindow(QMainWindow):
    """Main application window for Kira Calculator."""

    def __init__(
        self,
        history_service: HistoryService | None = None,
        settings_service: SettingsService | None = None,
    ) -> None:
        super().__init__()
        self.setWindowTitle("Kira Calculator")

        self.history_service = history_service or HistoryService()
        self.settings_service = settings_service or SettingsService()

        self.just_calculated = False
        self.display_is_error = False
        self.active_mode = "Standard"
        self.angle_mode = self.settings_service.settings.angle_mode

        self._init_window_geometry()
        self._create_ui()
        self._restore_settings()

    def _init_window_geometry(self) -> None:
        cfg = self.settings_service.settings
        self.resize(cfg.window_width, cfg.window_height)
        self.setMinimumSize(480, 520)

    def _create_ui(self) -> None:
        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        self.root_layout = QVBoxLayout(central)
        self.root_layout.setContentsMargins(10, 8, 10, 10)
        self.root_layout.setSpacing(8)

        # 1. Top Navigation Bar
        self.nav_bar = NavigationBar(self)
        self.nav_bar.mode_changed.connect(self.set_mode)
        self.nav_bar.theme_changed.connect(self._on_theme_changed)
        self.nav_bar.history_toggled.connect(self._toggle_history)
        self.root_layout.addWidget(self.nav_bar)

        # 2. Main content area: Left workspace + Right history drawer
        self.workspace_layout = QHBoxLayout()
        self.workspace_layout.setContentsMargins(0, 0, 0, 0)
        self.workspace_layout.setSpacing(10)

        # Calculator column
        self.calc_column = QVBoxLayout()
        self.calc_column.setSpacing(10)

        # Display widget (for Standard & Scientific)
        self.display = DisplayWidget(self)
        self.calc_column.addWidget(self.display)

        # Stacked pages
        self.stack = QStackedWidget()
        self.standard_page = StandardPage(self)
        self.scientific_page = ScientificPage(self)
        self.programmer_page = ProgrammerPage(self)
        self.converter_page = ConverterPage(self)

        self.stack.addWidget(self.standard_page)
        self.stack.addWidget(self.scientific_page)
        self.stack.addWidget(self.programmer_page)
        self.stack.addWidget(self.converter_page)

        self.calc_column.addWidget(self.stack, 1)

        calc_container = QWidget()
        calc_container.setLayout(self.calc_column)
        self.workspace_layout.addWidget(calc_container, 3)

        # History Drawer
        self.history_drawer = HistoryDrawer(self.history_service, self)
        self.history_drawer.entry_restored.connect(self._restore_history_expression)
        self.history_drawer.close_requested.connect(lambda: self._set_history_visible(False))
        self.history_drawer.setMinimumWidth(260)
        self.workspace_layout.addWidget(self.history_drawer, 1)

        self.root_layout.addLayout(self.workspace_layout, 1)

        # Connect button signals
        self.standard_page.button_clicked.connect(self._handle_standard_button)
        self.scientific_page.button_clicked.connect(self._handle_scientific_button)
        self.scientific_page.angle_mode_changed.connect(self._on_angle_mode_changed)

    def _restore_settings(self) -> None:
        cfg = self.settings_service.settings
        self.nav_bar.set_theme_choice(cfg.theme)
        self.set_mode(cfg.last_mode)
        self.scientific_page.set_angle_mode(cfg.angle_mode)
        self._set_history_visible(cfg.history_visible)

    def set_mode(self, mode_name: str) -> None:
        """Switch active calculation mode."""
        self.active_mode = mode_name
        self.nav_bar.set_active_mode(mode_name)

        mode_indices = {
            "Standard": 0,
            "Scientific": 1,
            "Programmer": 2,
            "Converter": 3,
        }
        idx = mode_indices.get(mode_name, 0)
        self.stack.setCurrentIndex(idx)

        # Standard and Scientific share expression display and history drawer
        is_expression_mode = mode_name in ("Standard", "Scientific")
        self.display.setVisible(is_expression_mode)
        if not is_expression_mode:
            self.history_drawer.setVisible(False)
            self.nav_bar.history_btn.setEnabled(False)
        else:
            self.history_drawer.setVisible(self.settings_service.settings.history_visible)
            self.nav_bar.history_btn.setEnabled(True)

        if mode_name == "Scientific":
            self.display.set_status(self.angle_mode)
        elif mode_name == "Standard":
            self.display.set_status("")

        self.settings_service.update(last_mode=mode_name)

    def _toggle_history(self) -> None:
        new_vis = not self.history_drawer.isVisible()
        self._set_history_visible(new_vis)

    def _set_history_visible(self, visible: bool) -> None:
        self.history_drawer.setVisible(visible)
        self.nav_bar.history_btn.setChecked(visible)
        self.settings_service.update(history_visible=visible)

    def _on_theme_changed(self, theme_key: str) -> None:
        app = QApplication.instance()
        if app:
            apply_theme(app, theme_key)
        self.settings_service.update(theme=theme_key)

    def _on_angle_mode_changed(self, mode: str) -> None:
        self.angle_mode = mode
        if self.active_mode == "Scientific":
            self.display.set_status(mode)
        self.settings_service.update(angle_mode=mode)

    # =========================================================================
    # Expression Input Handling
    # =========================================================================

    def _handle_standard_button(self, text: str) -> None:
        self._process_expression_input(text)

    def _handle_scientific_button(self, text: str) -> None:
        scientific_mappings = {
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
            "!": "!",
        }

        if text == "±":
            self._toggle_sign()
        elif text in scientific_mappings:
            self.append_text(scientific_mappings[text])
        else:
            self._process_expression_input(text)

    def _process_expression_input(self, text: str) -> None:
        if text == "C":
            self.clear_display()
        elif text == "⌫":
            self.backspace()
        elif text == "=":
            self.calculate_result()
        elif text == "±":
            self._toggle_sign()
        else:
            self.append_text(text)

    def _toggle_sign(self) -> None:
        curr = self.display.get_result()
        if self.display_is_error or curr == "0":
            return
        if curr.startswith("-"):
            self.display.set_result(curr[1:])
        else:
            self.display.set_result("-" + curr)

    def append_text(self, text: str) -> None:
        if self.display_is_error:
            self.display.set_result("0")
            self.display_is_error = False
            self.just_calculated = False

        curr = self.display.get_result()
        operators = ["+", "-", "×", "÷"]

        # Postfix and exponentiation continuation
        if text.startswith("^") or text in ("%", "!"):
            if self.just_calculated:
                self.just_calculated = False
            self.display.set_result(curr + text)
            return

        # Starting fresh after calculation when typing numbers
        if self.just_calculated:
            self.just_calculated = False
            if text in operators:
                # Continue calculation with previous result
                self.display.set_result(curr + text)
                return
            self.display.set_result(text)
            return

        # Prevent starting with multiplication or division
        if curr == "0" and text in ("×", "÷"):
            return

        # Replace operator if consecutively pressed
        if curr and curr[-1] in operators and text in operators:
            self.display.set_result(curr[:-1] + text)
            return

        # Prevent duplicate decimal in current token
        if text == ".":
            last_token = curr
            for op in operators:
                last_token = last_token.split(op)[-1]
            if "." in last_token:
                return

        if curr == "0" and text not in (".", "+", "-"):
            self.display.set_result(text)
        else:
            self.display.set_result(curr + text)

    def backspace(self) -> None:
        curr = self.display.get_result()
        if self.display_is_error or len(curr) <= 1:
            self.display.set_result("0")
            self.display_is_error = False
            return
        self.display.set_result(curr[:-1])

    def clear_display(self) -> None:
        self.display.clear()
        if self.active_mode == "Scientific":
            self.display.set_status(self.angle_mode)
        self.just_calculated = False
        self.display_is_error = False

    def calculate_result(self) -> None:
        expression = self.display.get_result()
        angle_mode = self.angle_mode if self.active_mode == "Scientific" else "DEG"

        res = evaluate_expression(expression, angle_mode=angle_mode)
        if res.success:
            self.display.set_expression(f"{expression} =")
            self.display.set_result(res.formatted_value)
            self.just_calculated = True
            self.display_is_error = False

            # Record in history
            entry = self.history_service.add_entry(
                expression=expression,
                result=res.formatted_value,
                mode=self.active_mode,
                details={"angle_mode": angle_mode},
            )
            self.history_drawer.add_entry(entry)
        else:
            self.display.set_result(res.formatted_value)
            self.just_calculated = False
            self.display_is_error = True

    def _restore_history_expression(self, expression: str) -> None:
        self.display.set_result(expression)
        self.display.set_expression("")
        self.just_calculated = False
        self.display_is_error = False

    # =========================================================================
    # Keyboard Event Handling
    # =========================================================================

    def keyPressEvent(self, event: QKeyEvent) -> None:
        # Global shortcuts for mode switching
        modifiers = event.modifiers()
        if modifiers & Qt.KeyboardModifier.ControlModifier:
            key = event.key()
            if key == Qt.Key.Key_1:
                self.set_mode("Standard")
                return
            if key == Qt.Key.Key_2:
                self.set_mode("Scientific")
                return
            if key == Qt.Key.Key_3:
                self.set_mode("Programmer")
                return
            if key == Qt.Key.Key_4:
                self.set_mode("Converter")
                return
            if key == Qt.Key.Key_H:
                if self.active_mode in ("Standard", "Scientific"):
                    self._toggle_history()
                return

        # Handle expression keys if in Standard or Scientific mode
        if self.active_mode in ("Standard", "Scientific"):
            key = event.key()
            text = event.text()

            if text.isdigit() or text in (".", "+", "-", "(", ")", "^", "%", "!"):
                self.append_text(text)
                return
            if text == "*":
                self.append_text("×")
                return
            if text == "/":
                self.append_text("÷")
                return
            if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                self.calculate_result()
                return
            if key == Qt.Key.Key_Backspace:
                self.backspace()
                return
            if key == Qt.Key.Key_Escape:
                self.clear_display()
                return

        super().keyPressEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:
        # Save geometry and state on exit
        self.settings_service.update(
            window_width=self.width(),
            window_height=self.height(),
            last_mode=self.active_mode,
            angle_mode=self.angle_mode,
            history_visible=self.history_drawer.isVisible(),
        )
        super().closeEvent(event)
