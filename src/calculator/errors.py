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
