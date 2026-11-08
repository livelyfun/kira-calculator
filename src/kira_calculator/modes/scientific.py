"""Scientific calculation mode facade."""

from __future__ import annotations

from ..core.engine import CalculationResult, calculate, evaluate_expression
from ..core.evaluator import AngleMode


class ScientificCalculator:
    """Facade for scientific calculations with angle mode awareness."""

    def __init__(self, angle_mode: AngleMode | str = AngleMode.DEG) -> None:
        self.angle_mode = angle_mode

    def calculate(self, expression: str) -> str:
        return calculate(expression, angle_mode=self.angle_mode)

    def evaluate(self, expression: str) -> CalculationResult:
        return evaluate_expression(expression, angle_mode=self.angle_mode)

