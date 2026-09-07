"""Session and optional persistent history for Kira Calculator."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List


class HistoryManager:
    """In-memory history with optional JSON persistence."""

    def __init__(self, max_entries: int = 100, persist_path: Path | None = None):
        self.max_entries = max_entries
        self.persist_path = persist_path
        self._entries: List[str] = []
        if persist_path and persist_path.exists():
            self._load()

    def add(self, expression: str, result: str) -> None:
        entry = f"{expression} = {result}"
        self._entries.insert(0, entry)
        if len(self._entries) > self.max_entries:
            self._entries = self._entries[: self.max_entries]
        self._save()

    def clear(self) -> None:
        self._entries.clear()
        self._save()

    def entries(self) -> List[str]:
        return list(self._entries)

    def _load(self) -> None:
        if not self.persist_path:
            return
        try:
            data = json.loads(self.persist_path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                self._entries = [str(x) for x in data][: self.max_entries]
        except Exception:  # noqa: BLE001
            self._entries = []

    def _save(self) -> None:
        if not self.persist_path:
            return
        try:
            self.persist_path.parent.mkdir(parents=True, exist_ok=True)
            self.persist_path.write_text(
                json.dumps(self._entries, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception:  # noqa: BLE001
            pass
