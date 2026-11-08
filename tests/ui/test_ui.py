"""UI integration tests using Qt offscreen platform."""

import os
import tempfile
import unittest
from pathlib import Path

# Ensure offscreen Qt platform before PySide6 initializes
os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PySide6.QtWidgets import QApplication

from kira_calculator.services.history_service import HistoryService
from kira_calculator.services.settings_service import SettingsService
from kira_calculator.ui.main_window import MainWindow

app = QApplication.instance() or QApplication([])


class TestMainWindowUI(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.history_service = HistoryService(Path(self.temp_dir.name) / "hist.json")
        self.settings_service = SettingsService(Path(self.temp_dir.name) / "set.json")
        self.window = MainWindow(
            history_service=self.history_service,
            settings_service=self.settings_service,
        )

    def tearDown(self):
        self.window.close()
        self.temp_dir.cleanup()

    def test_window_launch_and_initial_mode(self):
        self.assertEqual(self.window.windowTitle(), "Kira Calculator")
        self.assertEqual(self.window.active_mode, "Standard")
        self.assertEqual(self.window.display.get_result(), "0")

    def test_mode_switching(self):
        modes = ["Standard", "Scientific", "Programmer", "Converter"]
        for mode in modes:
            self.window.set_mode(mode)
            self.assertEqual(self.window.active_mode, mode)

    def test_standard_calculation_via_ui(self):
        self.window.set_mode("Standard")
        self.window.append_text("1")
        self.window.append_text("2")
        self.window.append_text("+")
        self.window.append_text("8")
        self.assertEqual(self.window.display.get_result(), "12+8")

        self.window.calculate_result()
        self.assertEqual(self.window.display.get_result(), "20")
        self.assertEqual(len(self.history_service.get_entries()), 1)

    def test_scientific_calculation_via_ui(self):
        self.window.set_mode("Scientific")
        self.window.clear_display()
        self.window._handle_scientific_button("sin")
        self.window.append_text("30")
        self.window.append_text(")")
        self.window.calculate_result()
        self.assertEqual(self.window.display.get_result(), "0.5")

    def test_programmer_page_interaction(self):
        self.window.set_mode("Programmer")
        page = self.window.programmer_page
        page.input.setText("15")
        page.refresh()
        self.assertEqual(page.value_labels[page.calculator.base].text(), "15")

    def test_converter_page_interaction(self):
        self.window.set_mode("Converter")
        conv = self.window.converter_page
        conv.from_input.setText("10")
        self.assertTrue(len(conv.to_input.text()) > 0)


if __name__ == "__main__":
    unittest.main()
