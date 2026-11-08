"""Modern calculation display widget showing expression, main result, and status."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
)


class DisplayWidget(QFrame):
    """Refined dual-line calculator display."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("displayFrame")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)

        # Top row: status (left) and expression (right)
        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)

        self.status_label = QLabel("")
        self.status_label.setObjectName("displayStatus")
        self.status_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        self.expression_label = QLabel("")
        self.expression_label.setObjectName("displayExpression")
        self.expression_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.expression_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        top_row.addWidget(self.status_label)
        top_row.addStretch()
        top_row.addWidget(self.expression_label)
        layout.addLayout(top_row)

        # Main result label (large, right aligned)
        self.result_label = QLabel("0")
        self.result_label.setObjectName("displayResult")
        self.result_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.result_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        self.result_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.result_label)

    def set_result(self, text: str) -> None:
        self.result_label.setText(text)

    def get_result(self) -> str:
        return self.result_label.text()

    def set_expression(self, text: str) -> None:
        self.expression_label.setText(text)

    def get_expression(self) -> str:
        return self.expression_label.text()

    def set_status(self, text: str) -> None:
        self.status_label.setText(text)

    def clear(self) -> None:
        self.result_label.setText("0")
        self.expression_label.setText("")
        self.status_label.setText("")
