"""Collapsible calculation history drawer with restore, copy, and clear functionality."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
)

from ...services.history_service import HistoryEntry, HistoryService


class HistoryDrawer(QFrame):
    """Side panel displaying persistent calculation history."""

    entry_restored = Signal(str)  # Emits expression to restore to calculator
    close_requested = Signal()

    def __init__(self, history_service: HistoryService, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("historyDrawer")
        self.history_service = history_service

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Header
        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        title = QLabel("History")
        title.setObjectName("historyHeaderTitle")
        header.addWidget(title)
        header.addStretch()

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setObjectName("navButton")
        self.clear_btn.setToolTip("Clear all calculation history")
        self.clear_btn.clicked.connect(self.clear_history)
        header.addWidget(self.clear_btn)

        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("iconButton")
        self.close_btn.setToolTip("Close history panel")
        self.close_btn.clicked.connect(self.close_requested.emit)
        header.addWidget(self.close_btn)

        layout.addLayout(header)

        # History list
        self.list_widget = QListWidget()
        self.list_widget.setObjectName("historyList")
        self.list_widget.itemDoubleClicked.connect(self._on_item_double_clicked)
        layout.addWidget(self.list_widget)

        # Footer actions
        footer = QHBoxLayout()
        self.copy_btn = QPushButton("Copy Result")
        self.copy_btn.setObjectName("navButton")
        self.copy_btn.clicked.connect(self._copy_selected_result)
        footer.addWidget(self.copy_btn)
        layout.addLayout(footer)

        self.refresh()

    def refresh(self) -> None:
        """Reload list from history service."""
        self.list_widget.clear()
        entries = self.history_service.get_entries()
        for entry in entries:
            text = f"{entry.expression} = {entry.result}"
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, entry)
            item.setToolTip(f"Mode: {entry.mode}\nDouble-click to reuse expression")
            self.list_widget.addItem(item)

    def add_entry(self, entry: HistoryEntry) -> None:
        """Prepend new entry dynamically."""
        text = f"{entry.expression} = {entry.result}"
        item = QListWidgetItem(text)
        item.setData(Qt.ItemDataRole.UserRole, entry)
        item.setToolTip(f"Mode: {entry.mode}\nDouble-click to reuse expression")
        self.list_widget.insertItem(0, item)

    def clear_history(self) -> None:
        self.history_service.clear()
        self.list_widget.clear()

    def _on_item_double_clicked(self, item: QListWidgetItem) -> None:
        entry: HistoryEntry | None = item.data(Qt.ItemDataRole.UserRole)
        if entry:
            self.entry_restored.emit(entry.expression)
        else:
            text = item.text().split("=")[0].strip()
            self.entry_restored.emit(text)

    def _copy_selected_result(self) -> None:
        item = self.list_widget.currentItem()
        if not item:
            return
        entry: HistoryEntry | None = item.data(Qt.ItemDataRole.UserRole)
        if entry:
            clipboard = QApplication.clipboard()
            clipboard.setText(entry.result)
        else:
            parts = item.text().split("=")
            if len(parts) > 1:
                QApplication.clipboard().setText(parts[1].strip())

