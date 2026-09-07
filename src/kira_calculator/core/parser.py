"""Symbol normalisation for the calculator expression engine."""

from __future__ import annotations


def prepare_expression(expression: str) -> str:
    """
    Convert calculator UI symbols into Python / asteval-compatible operators
    and function names.
    """
    if not expression or not expression.strip():
        return "0"

    expr = expression.strip()

    # UI operators → Python
    replacements = {
        "×": "*",
        "÷": "/",
        "√": "sqrt",
        "π": "pi",
        "x²": "**2",
        "xʸ": "**",
        "¹⁄ₓ": "1/",  # just in case
    }

    for old, new in replacements.items():
        expr = expr.replace(old, new)

    # Common aliases that may appear from buttons
    expr = expr.replace("ln(", "log(")  # natural log → math.log

    return expr
