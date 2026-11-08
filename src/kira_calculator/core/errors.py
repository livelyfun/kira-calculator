"""Typed exception hierarchy for Kira Calculator engines."""

from __future__ import annotations


class CalculatorError(Exception):
    """Base exception for all Kira Calculator errors."""

    def __init__(self, message: str, position: int | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.position = position

    def __str__(self) -> str:
        if self.position is not None:
            return f"{self.message} (at character {self.position})"
        return self.message


class CalculatorSyntaxError(CalculatorError):
    """Raised when an expression has invalid syntax or malformed structure."""


class InvalidNumberError(CalculatorError):
    """Raised when a number literal cannot be parsed."""


class UnknownFunctionError(CalculatorError):
    """Raised when an unrecognized function identifier is encountered."""


class UnknownConstantError(CalculatorError):
    """Raised when an unrecognized constant identifier is encountered."""


class DivisionByZeroError(CalculatorError):
    """Raised on arithmetic division by zero or modulo by zero."""


class CalculatorDomainError(CalculatorError):
    """Raised when a mathematical operation is outside its valid domain."""


class CalculatorOverflowError(CalculatorError):
    """Raised when a computation overflows numerical representation limits."""


class SecurityError(CalculatorError):
    """Raised when an expression violates security constraints or resource limits."""


# ============================================================================
# Programmer Calculator Exceptions
# ============================================================================


class ProgrammerError(CalculatorError):
    """Base exception for programmer mode operations."""


class InvalidProgrammerNumberError(ProgrammerError):
    """Raised when a number literal is invalid for the current radix/range."""


class ProgrammerDivisionByZeroError(ProgrammerError):
    """Raised on integer division or modulo by zero in programmer mode."""


class ProgrammerShiftError(ProgrammerError):
    """Raised when a shift count is negative or exceeds word size."""


# ============================================================================
# Unit Converter Exceptions
# ============================================================================


class ConverterError(CalculatorError):
    """Base exception for unit converter operations."""


class UnknownUnitError(ConverterError):
    """Raised when a requested unit is not recognized."""


class IncompatibleUnitError(ConverterError):
    """Raised when converting between mismatched unit categories."""

