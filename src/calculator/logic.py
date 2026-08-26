"""High-level calculation interface connecting Tokenizer, Parser, and Evaluator."""

import math
from dataclasses import dataclass

from .errors import CalculatorError
from .evaluator import AngleMode, Evaluator
from .parser import Parser
from .tokenizer import tokenize


@dataclass(frozen=True)
class CalculationResult:
    """Represents the structured result of an evaluated expression."""

    success: bool
    formatted_value: str
    numeric_value: float | None = None
    error: CalculatorError | None = None
    error_message: str | None = None


def format_number(value: float, precision: int = 12) -> str:
    """Format a floating-point number cleanly for calculator display.

    - Whole numbers are formatted as integers (e.g. 5.0 -> '5').
    - Floating point representation inaccuracies are cleaned (e.g. 0.30000000000000004 -> '0.3').
    - Extremely large or tiny numbers use clean scientific notation.
    """
    if math.isnan(value):
        return "NaN"
    if math.isinf(value):
        return "Infinity" if value > 0 else "-Infinity"

    # Check for near-integer values
    rounded = round(value, precision)
    if math.isclose(value, round(value), abs_tol=1e-11):
        int_val = int(round(value))
        return str(int_val)

    # Use scientific notation for very large or tiny magnitudes
    abs_val = abs(rounded)
    if (abs_val >= 1e15) or (0 < abs_val < 1e-9):
        formatted = f"{rounded:.8e}"
        # Clean up exponent formatting (e.g. 1.2000e+05 -> 1.2e+5)
        base, exp = formatted.split("e")
        base = base.rstrip("0").rstrip(".")
        exp_int = int(exp)
        return f"{base}e{exp_int}"

    # Standard decimal representation
    formatted = f"{rounded:.{precision}f}".rstrip("0").rstrip(".")
    if formatted in ("-0", "-0."):
        return "0"
    return formatted


def evaluate_expression(
    expression: str, angle_mode: str | AngleMode = "DEG"
) -> CalculationResult:
    """Parse and evaluate a mathematical expression, returning a structured CalculationResult."""
    try:
        tokens = tokenize(expression)
        parser = Parser(tokens)
        ast = parser.parse()
        evaluator = Evaluator(angle_mode=angle_mode)
        numeric_result = evaluator.evaluate(ast)
        formatted = format_number(numeric_result)

        return CalculationResult(
            success=True,
            formatted_value=formatted,
            numeric_value=numeric_result,
        )

    except CalculatorError as err:
        return CalculationResult(
            success=False,
            formatted_value=err.message,
            numeric_value=None,
            error=err,
            error_message=err.message,
        )
    except Exception as err:
        return CalculationResult(
            success=False,
            formatted_value=f"Error: {err}",
            numeric_value=None,
            error_message=str(err),
        )


def calculate(expression: str, angle_mode: str | AngleMode = "DEG") -> str:
    """Convenience function returning the formatted string result or error message."""
    result = evaluate_expression(expression, angle_mode=angle_mode)
    return result.formatted_value
