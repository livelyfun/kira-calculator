from PySide6.QtCore import Signal
from PySide6.QtWidgets import QButtonGroup, QHBoxLayout, QPushButton, QWidget

try:
    from src.ui.modes import AppMode
except ImportError:
    from ui.modes import AppMode


class ModeBar(QWidget):
    """Top-level mode navigation backed by :class:`AppMode`."""

    mode_selected = Signal(object)

    def __init__(self) -> None:
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        self.buttons: dict[AppMode, QPushButton] = {}
        for index, mode in enumerate(AppMode):
            button = QPushButton(mode.label)
            button.setObjectName("modeButton")
            button.setCheckable(True)
            self.button_group.addButton(button, index)
            layout.addWidget(button)
            self.buttons[mode] = button

        self.standard_button = self.buttons[AppMode.STANDARD]
        self.scientific_button = self.buttons[AppMode.SCIENTIFIC]
        self.programmer_button = self.buttons[AppMode.PROGRAMMER]
        self.converter_button = self.buttons[AppMode.CONVERTER]
        self.button_group.idClicked.connect(self._mode_clicked)

        self.set_active_mode(AppMode.STANDARD)

    @property
    def active_mode(self) -> AppMode:
        """Return the currently selected application mode."""
        return next(mode for mode, button in self.buttons.items() if button.isChecked())

    def set_active_mode(self, mode: AppMode) -> None:
        """Reflect a programmatic mode change in the navigation controls."""
        self.buttons[mode].setChecked(True)

    def _mode_clicked(self, index: int) -> None:
        self.mode_selected.emit(tuple(AppMode)[index])
