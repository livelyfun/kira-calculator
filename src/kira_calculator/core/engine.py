"""Unified mathematical calculation engine coordinating tokenization, parsing, and evaluation."""

from __future__ import annotations

from dataclasses import dataclass

from .errors import CalculatorError
from .evaluator import AngleMode, Evaluator
from .formatter import format_number
from .parser import Parser
from .tokenizer import tokenize


@dataclass(frozen=True)
class CalculationResult:
    """Represents the structured result of an expression evaluation."""

    expression: str
    success: bool
    raw_value: float | None
    formatted_value: str
    error: CalculatorError | None
    angle_mode: str


def evaluate_expression(
    expression: str, angle_mode: AngleMode | str = AngleMode.DEG
) -> CalculationResult:
    """Evaluate an expression string safely and return a CalculationResult.

    Args:
        expression: Mathematical expression string.
        angle_mode: Angle mode to interpret trigonometric arguments (DEG, RAD, GRAD).

    Returns:
        CalculationResult with numerical value or typed error.
    """
    cleaned = expression.strip()
    if not cleaned:
        return CalculationResult(
            expression=expression,
            success=False,
            raw_value=None,
            formatted_value="Error: Empty expression",
            error=CalculatorError("Empty expression"),
            angle_mode=str(angle_mode),
        )

    try:
        tokens = tokenize(cleaned)
        parser = Parser(tokens)
        ast = parser.parse()
        evaluator = Evaluator(angle_mode=angle_mode)
        raw = evaluator.evaluate(ast)
        formatted = format_number(raw)
        return CalculationResult(
            expression=expression,
            success=True,
            raw_value=raw,
            formatted_value=formatted,
            error=None,
            angle_mode=str(angle_mode),
        )
    except CalculatorError as err:
        return CalculationResult(
            expression=expression,
            success=False,
            raw_value=None,
            formatted_value=f"Error: {err.message}",
            error=err,
            angle_mode=str(angle_mode),
        )
    except Exception as err:
        return CalculationResult(
            expression=expression,
            success=False,
            raw_value=None,
            formatted_value=f"Error: {err}",
            error=CalculatorError(str(err)),
            angle_mode=str(angle_mode),
        )


def calculate(expression: str, angle_mode: AngleMode | str = AngleMode.DEG) -> str:
    """Simple string-in string-out entry point for UI displays."""
    res = evaluate_expression(expression, angle_mode)
    if res.success:
        return res.formatted_value
    # In standard UI display, if it begins with "Error: ", return it or the message
    return res.formatted_value

