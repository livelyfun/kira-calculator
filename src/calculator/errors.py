"""Custom exceptions for Kira Calculator expression engine."""


class CalculatorError(Exception):
    """Base class for all calculator errors."""

    def __init__(self, message: str, position: int | None = None):
        super().__init__(message)
        self.message = message
        self.position = position

    def __str__(self) -> str:
        if self.position is not None:
            return f"{self.message} at position {self.position}"
        return self.message


class CalculatorSyntaxError(CalculatorError):
    """Raised when an expression has invalid syntax or cannot be parsed."""


class CalculatorDomainError(CalculatorError):
    """Raised when a mathematical function is called outside its valid domain."""


class DivisionByZeroError(CalculatorError):
    """Raised when division or modulo by zero occurs."""


class UnknownFunctionError(CalculatorError):
    """Raised when an unrecognized function name is encountered."""


class UnknownConstantError(CalculatorError):
    """Raised when an unrecognized constant name is encountered."""


class InvalidNumberError(CalculatorError):
    """Raised when a number literal is malformed."""


class CalculatorOverflowError(CalculatorError):
    """Raised when a calculation exceeds floating point representation limits."""


class ProgrammerError(CalculatorError):
    """Base class for programmer-mode integer errors."""


class InvalidProgrammerNumberError(ProgrammerError):
    """Raised when a value is invalid for the selected number base."""


class ProgrammerDivisionByZeroError(ProgrammerError):
    """Raised when programmer-mode division uses a zero divisor."""


class ProgrammerShiftError(ProgrammerError):
    """Raised when a shift count is negative or exceeds the word size."""
