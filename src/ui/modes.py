"""Application mode definitions shared by navigation and the window shell."""

from enum import Enum


class AppMode(str, Enum):
    """Stable identifiers for the calculator's top-level application modes."""

    STANDARD = "standard"
    SCIENTIFIC = "scientific"
    PROGRAMMER = "programmer"
    CONVERTER = "converter"

    @property
    def label(self) -> str:
        """Return the user-facing label for this mode."""
        return {
            AppMode.STANDARD: "Standard",
            AppMode.SCIENTIFIC: "Scientific",
            AppMode.PROGRAMMER: "Programmer",
            AppMode.CONVERTER: "Converter",
        }[self]

    @property
    def uses_expression_model(self) -> bool:
        """Whether this mode uses the shared expression display and history."""
        return self in (AppMode.STANDARD, AppMode.SCIENTIFIC)
