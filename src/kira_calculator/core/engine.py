"""
Safe expression evaluation engine for Kira Calculator.

Uses asteval with a restricted math namespace. Never uses bare eval().
"""

from __future__ import annotations

import math
from typing import Any

from asteval import Interpreter

from .parser import prepare_expression

# Shared interpreter – created once
_aeval: Interpreter | None = None


def _get_interpreter() -> Interpreter:
    global _aeval
    if _aeval is None:
        _aeval = Interpreter(
            use_numpy=False,
            minimal=False,
            no_print=True,
        )
        # Safe math symbols
        safe_math = {
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "asin": math.asin,
            "acos": math.acos,
            "atan": math.atan,
            "sinh": math.sinh,
            "cosh": math.cosh,
            "tanh": math.tanh,
            "log": math.log,          # natural log
            "log10": math.log10,
            "ln": math.log,           # alias
            "sqrt": math.sqrt,
            "fabs": math.fabs,
            "abs": abs,
            "ceil": math.ceil,
            "floor": math.floor,
            "pow": math.pow,
            "exp": math.exp,
            "pi": math.pi,
            "e": math.e,
            "tau": math.tau,
            "inf": math.inf,
            "nan": math.nan,
        }
        _aeval.symtable.update(safe_math)
        # Disable dangerous names
        for name in ("import", "open", "exec", "eval", "compile", "__import__", "getattr", "setattr"):
            _aeval.symtable.pop(name, None)
    return _aeval


def evaluate(expression: str) -> str:
    """
    Evaluate a calculator expression safely.

    Returns the result as a string, or "Error" on any failure.
    """
    try:
        prepared = prepare_expression(expression)
        interpreter = _get_interpreter()
        result: Any = interpreter(prepared)

        if result is None:
            return "Error"

        # Clean whole floats → int
        if isinstance(result, float):
            if math.isnan(result) or math.isinf(result):
                return str(result)
            if result.is_integer():
                result = int(result)

        return str(result)
    except Exception:  # noqa: BLE001 – intentional catch-all for UI
        return "Error"


def calculate(expression: str) -> str:
    """Public entry point used by the UI."""
    return evaluate(expression)
