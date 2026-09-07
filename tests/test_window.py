"""Focused, headless tests for calculator-window state transitions."""

import os

import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QApplication

from src.calculator.programmer import NumberBase
from src.ui.modes import AppMode
from src.ui.window import CalculatorWindow
from src.widgets.programmer_page import ProgrammerPage


@pytest.fixture(scope="module")
def application() -> QApplication:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    return QApplication.instance() or QApplication([])


def test_input_replaces_error_message(application: QApplication) -> None:
    window = CalculatorWindow()
    window.display.setText("sqrt(-1)")
    window.calculate_result()

    assert "undefined" in window.display.text().lower()

    window.append_text("7")

    assert window.display.text() == "7"
    window.close()


def test_backspace_clears_error_message(application: QApplication) -> None:
    window = CalculatorWindow()
    window.display.setText("sin(90, 0)")
    window.calculate_result()

    window.backspace()

    assert window.display.text() == "0"
    window.close()


def test_programmer_page_converts_values_and_updates_bits(
    application: QApplication,
) -> None:
    page = ProgrammerPage()
    page.word_size_selector.setCurrentText("8-bit")
    page.input.setText("255")

    assert page.value_labels[NumberBase.BIN].text() == "11111111"
    assert page.bits.text() == "11111111"

    page.base_selector.setCurrentText("HEX")
    page.input.setText("FF")
    assert page.value_labels[NumberBase.DEC].text() == "255"
    page.close()


def test_window_switches_between_calculator_and_programmer_modes(
    application: QApplication,
) -> None:
    window = CalculatorWindow()

    window.mode_bar.programmer_button.click()
    assert window.stack.currentWidget() is window.programmer_page
    assert window.display.isHidden()

    window.mode_bar.standard_button.click()
    assert window.stack.currentWidget() is window.calculator_page
    assert not window.display.isHidden()
    window.close()


def test_standard_is_the_default_mode(application: QApplication) -> None:
    window = CalculatorWindow()

    assert window.active_mode == AppMode.STANDARD
    assert window.mode_bar.active_mode == AppMode.STANDARD
    assert window.stack.currentWidget() is window.calculator_page
    assert not window.display.isHidden()
    assert not window.history_widget.isHidden()
    window.close()


def test_standard_and_scientific_controls_are_explicit(
    application: QApplication,
) -> None:
    window = CalculatorWindow()

    assert {"+", "-", "×", "÷", ".", "(", ")", "C", "⌫", "="} <= set(
        window.calculator_page.buttons
    )
    assert not {"sin", "log", "π", "x²"} & set(window.calculator_page.buttons)
    assert {
        "sin",
        "asin",
        "sinh",
        "√",
        "!",
        "π",
        "x²",
    } <= set(window.scientific_page.buttons)
    assert window.scientific_page.angle_selector.currentText() == "DEG"
    window.close()


def test_scientific_controls_write_to_the_shared_expression_display(
    application: QApplication,
) -> None:
    window = CalculatorWindow()

    window.set_mode(AppMode.SCIENTIFIC)
    window.scientific_page.buttons["asin"].click()

    assert window.display.text() == "asin("
    window.close()


@pytest.mark.parametrize(
    ("mode", "page_name"),
    [
        (AppMode.STANDARD, "calculator_page"),
        (AppMode.SCIENTIFIC, "scientific_page"),
        (AppMode.PROGRAMMER, "programmer_page"),
        (AppMode.CONVERTER, "converter_page"),
    ],
)
def test_each_explicit_mode_can_be_selected(
    application: QApplication, mode: AppMode, page_name: str
) -> None:
    window = CalculatorWindow()

    window.set_mode(mode)

    assert window.active_mode == mode
    assert window.mode_bar.active_mode == mode
    assert window.stack.currentWidget() is getattr(window, page_name)
    assert window.display.isHidden() is not mode.uses_expression_model
    assert window.history_widget.isHidden() is not mode.uses_expression_model
    window.close()


@pytest.mark.parametrize("source", list(AppMode))
@pytest.mark.parametrize("target", list(AppMode))
def test_every_mode_transition_updates_the_active_page(
    application: QApplication, source: AppMode, target: AppMode
) -> None:
    window = CalculatorWindow()

    window.set_mode(source)
    window.set_mode(target)

    assert window.active_mode == target
    assert window.mode_bar.active_mode == target
    assert window.stack.currentWidget() is window.pages[target]
    window.close()


def test_mode_bar_selects_all_modes(application: QApplication) -> None:
    window = CalculatorWindow()

    for mode, button in window.mode_bar.buttons.items():
        button.click()
        assert window.active_mode == mode

    window.close()


def test_global_expression_keys_do_not_cross_into_programmer_mode(
    application: QApplication,
) -> None:
    window = CalculatorWindow()
    window.display.setText("42")
    window.programmer_page.input.setText("0")
    window.set_mode(AppMode.PROGRAMMER)

    event = QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key.Key_7, Qt.NoModifier, "7")
    window.keyPressEvent(event)

    assert window.display.text() == "42"
    assert window.programmer_page.input.text() == "0"
    window.close()


def test_standard_mode_does_not_accept_scientific_keyboard_operators(
    application: QApplication,
) -> None:
    window = CalculatorWindow()
    window.display.setText("2")

    event = QKeyEvent(
        QKeyEvent.Type.KeyPress, Qt.Key.Key_AsciiCircum, Qt.NoModifier, "^"
    )
    window.keyPressEvent(event)

    assert window.display.text() == "2"
    window.close()
