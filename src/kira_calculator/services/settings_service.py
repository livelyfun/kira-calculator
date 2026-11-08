"""Persistent application settings service with atomic writes and safe defaults."""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class AppSettings:
    """Strongly typed application configuration settings."""

    theme: str = "dark"
    window_width: int = 920
    window_height: int = 680
    last_mode: str = "Standard"
    angle_mode: str = "DEG"
    precision: int = 12
    history_visible: bool = True
    programmer_base: str = "DEC"
    programmer_word_size: str = "32-bit"
    programmer_signed: bool = False
    converter_category: str = "Length"
    converter_from_unit: str = "Meter (m)"
    converter_to_unit: str = "Foot (ft)"


def get_default_config_dir() -> Path:
    """Determine platform-appropriate configuration directory."""
    if sys.platform.startswith("linux"):
        xdg_config = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config:
            base = Path(xdg_config)
        else:
            base = Path.home() / ".config"
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    elif sys.platform == "win32":
        app_data = os.environ.get("APPDATA")
        base = Path(app_data) if app_data else Path.home() / "AppData" / "Roaming"
    else:
        base = Path.home() / ".config"

    path = base / "kira-calculator"
    path.mkdir(parents=True, exist_ok=True)
    return path


class SettingsService:
    """Manages loading, updating, and atomic persistence of user preferences."""

    def __init__(self, storage_path: Path | None = None) -> None:
        if storage_path is None:
            storage_path = get_default_config_dir() / "settings.json"
        self.storage_path = storage_path
        self._settings = AppSettings()
        self.load()

    @property
    def settings(self) -> AppSettings:
        return self._settings

    def load(self) -> AppSettings:
        """Safely load settings from disk with fallback to safe defaults."""
        if not self.storage_path.exists():
            return self._settings

        try:
            with open(self.storage_path, encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, dict):
                # Update known fields
                for field_name in asdict(self._settings):
                    if field_name in data:
                        val = data[field_name]
                        # Type coerce
                        expected_type = type(getattr(self._settings, field_name))
                        try:
                            setattr(self._settings, field_name, expected_type(val))
                        except (ValueError, TypeError):
                            pass
        except (json.JSONDecodeError, OSError):
            # Safe recovery on corrupt file
            pass

        return self._settings

    def save(self) -> None:
        """Atomically write settings to disk."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.storage_path.with_suffix(".tmp")

        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(asdict(self._settings), f, indent=2)
                f.flush()
                os.fsync(f.fileno())

            os.replace(temp_path, self.storage_path)
        except OSError:
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except OSError:
                    pass

    def update(self, **kwargs: Any) -> None:
        """Update one or more settings and persist."""
        modified = False
        for key, value in kwargs.items():
            if hasattr(self._settings, key):
                current = getattr(self._settings, key)
                if current != value:
                    setattr(self._settings, key, value)
                    modified = True
        if modified:
            self.save()
