"""Focused, headless tests for calculator-window state transitions."""

import os

import pytest
from PySide6.QtWidgets import QApplication

from src.ui.window import CalculatorWindow


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
