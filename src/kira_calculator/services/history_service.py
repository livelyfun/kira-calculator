"""Persistent calculation history service with atomic writes and validation."""

from __future__ import annotations

import json
import os
import sys
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class HistoryEntry:
    """Represents a single persistent calculation record."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    expression: str = ""
    result: str = ""
    mode: str = "Standard"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    details: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> HistoryEntry:
        return cls(
            id=str(data.get("id", uuid.uuid4())),
            expression=str(data.get("expression", "")),
            result=str(data.get("result", "")),
            mode=str(data.get("mode", "Standard")),
            timestamp=str(data.get("timestamp", "")),
            details=dict(data.get("details", {})),
        )


def get_default_data_dir() -> Path:
    """Determine standard platform-specific data directory."""
    if sys.platform.startswith("linux"):
        xdg_data = os.environ.get("XDG_DATA_HOME")
        if xdg_data:
            base = Path(xdg_data)
        else:
            base = Path.home() / ".local" / "share"
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    elif sys.platform == "win32":
        app_data = os.environ.get("APPDATA")
        base = Path(app_data) if app_data else Path.home() / "AppData" / "Roaming"
    else:
        base = Path.home() / ".kira-calculator"

    path = base / "kira-calculator"
    path.mkdir(parents=True, exist_ok=True)
    return path


class HistoryService:
    """Manages reading, adding, clearing, and atomic persistence of calculation history."""

    MAX_HISTORY_ENTRIES = 500

    def __init__(self, storage_path: Path | None = None) -> None:
        if storage_path is None:
            storage_path = get_default_data_dir() / "history.json"
        self.storage_path = storage_path
        self._entries: list[HistoryEntry] = []
        self.load()

    def load(self) -> list[HistoryEntry]:
        """Safely load history from disk, handling malformed files gracefully."""
        if not self.storage_path.exists():
            self._entries = []
            return self._entries

        try:
            with open(self.storage_path, encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, list):
                self._entries = [
                    HistoryEntry.from_dict(item)
                    for item in data
                    if isinstance(item, dict) and "expression" in item
                ]
            else:
                self._entries = []
        except (json.JSONDecodeError, OSError, ValueError):
            # Safe recovery on corrupted or partially written file
            self._entries = []

        return self._entries

    def save(self) -> None:
        """Atomically persist history entries to disk."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.storage_path.with_suffix(".tmp")

        try:
            serialized = [asdict(e) for e in self._entries[: self.MAX_HISTORY_ENTRIES]]
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(serialized, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())

            # Atomic replace
            os.replace(temp_path, self.storage_path)
        except OSError:
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except OSError:
                    pass

    def add_entry(
        self,
        expression: str,
        result: str,
        mode: str = "Standard",
        details: dict[str, Any] | None = None,
    ) -> HistoryEntry:
        """Record a calculation and save atomically."""
        entry = HistoryEntry(
            expression=expression,
            result=result,
            mode=mode,
            details=details or {},
        )
        self._entries.insert(0, entry)
        if len(self._entries) > self.MAX_HISTORY_ENTRIES:
            self._entries = self._entries[: self.MAX_HISTORY_ENTRIES]
        self.save()
        return entry

    def get_entries(self) -> list[HistoryEntry]:
        """Return shallow copy of in-memory entries."""
        return list(self._entries)

    def clear(self) -> None:
        """Clear all entries and update persistent storage."""
        self._entries.clear()
        self.save()

    def remove_entry(self, entry_id: str) -> bool:
        """Remove an entry by ID."""
        initial_len = len(self._entries)
        self._entries = [e for e in self._entries if e.id != entry_id]
        if len(self._entries) != initial_len:
            self.save()
            return True
        return False
