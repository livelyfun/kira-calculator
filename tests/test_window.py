"""Focused, headless tests for calculator-window state transitions."""

import os

import pytest
from PySide6.QtWidgets import QApplication

from src.calculator.programmer import NumberBase
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

    window.mode_bar.calculator_button.click()
    assert window.stack.currentWidget() is window.calculator_page
    assert not window.display.isHidden()
    window.close()
