"""Standard calculation mode facade."""

from __future__ import annotations

from ..core.engine import CalculationResult, calculate, evaluate_expression


class StandardCalculator:
    """Facade for standard arithmetic operations."""

    @staticmethod
    def calculate(expression: str) -> str:
        return calculate(expression)

    @staticmethod
    def evaluate(expression: str) -> CalculationResult:
        return evaluate_expression(expression)
