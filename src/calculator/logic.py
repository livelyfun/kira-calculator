"""Backward-compatible facade delegating to the secure kira_calculator engine."""

from __future__ import annotations

from kira_calculator.core.engine import (
    CalculationResult,
    calculate,
    evaluate_expression,
)
from kira_calculator.core.formatter import format_number

__all__ = [
    "CalculationResult",
    "calculate",
    "evaluate_expression",
    "format_number",
]
