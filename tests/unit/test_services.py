"""Unit tests for HistoryService and SettingsService persistence."""

import tempfile
import unittest
from pathlib import Path

from kira_calculator.services.history_service import HistoryService
from kira_calculator.services.settings_service import SettingsService


class TestServices(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.history_file = Path(self.temp_dir.name) / "history.json"
        self.settings_file = Path(self.temp_dir.name) / "settings.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_history_lifecycle(self):
        service = HistoryService(storage_path=self.history_file)
        self.assertEqual(len(service.get_entries()), 0)

        entry1 = service.add_entry("2 + 2", "4", "Standard")
        self.assertEqual(len(service.get_entries()), 1)
        self.assertEqual(service.get_entries()[0].expression, "2 + 2")

        # Persistence across reload
        reloaded = HistoryService(storage_path=self.history_file)
        self.assertEqual(len(reloaded.get_entries()), 1)
        self.assertEqual(reloaded.get_entries()[0].id, entry1.id)

        # Clear
        reloaded.clear()
        self.assertEqual(len(reloaded.get_entries()), 0)
        self.assertEqual(len(HistoryService(storage_path=self.history_file).get_entries()), 0)

    def test_history_corrupt_file_recovery(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            f.write("{ invalid json [")

        service = HistoryService(storage_path=self.history_file)
        # Safely recovers to empty list rather than crashing
        self.assertEqual(service.get_entries(), [])
        # Able to save new entries cleanly
        service.add_entry("3 * 3", "9")
        self.assertEqual(len(service.get_entries()), 1)

    def test_settings_lifecycle(self):
        service = SettingsService(storage_path=self.settings_file)
        self.assertEqual(service.settings.theme, "dark")
        self.assertEqual(service.settings.last_mode, "Standard")

        service.update(theme="light", last_mode="Scientific", angle_mode="RAD")
        self.assertEqual(service.settings.theme, "light")

        # Reload from disk
        reloaded = SettingsService(storage_path=self.settings_file)
        self.assertEqual(reloaded.settings.theme, "light")
        self.assertEqual(reloaded.settings.last_mode, "Scientific")
        self.assertEqual(reloaded.settings.angle_mode, "RAD")

    def test_settings_corrupt_file_recovery(self):
        with open(self.settings_file, "w", encoding="utf-8") as f:
            f.write("corrupted garbage content")

        service = SettingsService(storage_path=self.settings_file)
        # Safe defaults applied
        self.assertEqual(service.settings.theme, "dark")
        self.assertEqual(service.settings.window_width, 920)


if __name__ == "__main__":
    unittest.main()

