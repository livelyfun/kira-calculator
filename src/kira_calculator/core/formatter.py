"""Number formatting and normalization utilities for calculation results."""

from __future__ import annotations

import math
from decimal import Decimal, InvalidOperation


def format_number(value: float, max_precision: int = 12) -> str:
    """Format a numerical result with smart precision and noise suppression.

    Args:
        value: The floating-point number to format.
        max_precision: Maximum significant digits or decimal places.

    Returns:
        A clean, human-readable string representation.
    """
    if math.isnan(value):
        return "NaN"
    if math.isinf(value):
        return "-Infinity" if value < 0 else "Infinity"

    # Exact or near integer check
    if math.isclose(value, round(value), abs_tol=1e-12):
        int_val = int(round(value))
        # Check if integer fits within standard display or needs scientific
        if abs(int_val) >= 10**15:
            return f"{value:.{max_precision}e}".replace("e+", "e")
        return str(int_val)

    # For very large or very small magnitudes, use scientific notation
    abs_val = abs(value)
    if abs_val >= 10**14 or (0 < abs_val < 1e-6):
        # Format in scientific notation and trim trailing zeros
        formatted = f"{value:.{min(max_precision, 10)}e}"
        mantissa, exp = formatted.split("e")
        mantissa = mantissa.rstrip("0").rstrip(".")
        exp_int = int(exp)
        return f"{mantissa}e{exp_int}"

    # For standard decimals, eliminate IEEE 754 precision noise using Decimal quantize
    try:
        # Round to max_precision significant digits
        d = Decimal(str(value))
        # Quantize to 12 decimal places to eliminate noise like .30000000000000004
        rounded = round(float(d), max_precision)
        if rounded.is_integer():
            return str(int(rounded))
        # Format string stripping redundant trailing zeros
        str_val = f"{rounded:.{max_precision}f}".rstrip("0").rstrip(".")
        return str_val
    except (InvalidOperation, ValueError):
        return str(value)

