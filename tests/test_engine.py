"""Unit tests for the safe expression engine."""

from __future__ import annotations

import math

import pytest

from kira_calculator.core import calculate, prepare_expression


class TestPrepareExpression:
    def test_operators(self):
        assert prepare_expression("2×3") == "2*3"
        assert prepare_expression("8÷2") == "8/2"

    def test_symbols(self):
        assert "pi" in prepare_expression("π")
        assert "sqrt" in prepare_expression("√")

    def test_empty(self):
        assert prepare_expression("") == "0"
        assert prepare_expression("   ") == "0"


class TestCalculate:
    def test_basic_arithmetic(self):
        assert calculate("2+2") == "4"
        assert calculate("10-3") == "7"
        assert calculate("4×5") == "20"
        assert calculate("9÷3") == "3"

    def test_precedence(self):
        assert calculate("2+3×4") == "14"
        assert calculate("(2+3)×4") == "20"

    def test_scientific(self):
        assert calculate("sin(0)") == "0"
        assert calculate("cos(0)") == "1"
        assert abs(float(calculate("pi")) - math.pi) < 1e-10
        assert calculate("sqrt(16)") == "4"
        assert calculate("2**3") == "8"
        assert calculate("e")  # just check it doesn't error

    def test_log(self):
        assert calculate("log10(100)") == "2"
        # ln is aliased to math.log
        result = float(calculate("ln(e)"))
        assert abs(result - 1.0) < 1e-10

    def test_error_handling(self):
        assert calculate("1/0") == "Error" or "inf" in calculate("1/0").lower()
        assert calculate("sin(") == "Error"
        assert calculate("unknown_func(1)") == "Error"

    def test_integer_cleanup(self):
        assert calculate("4.0") == "4"
        assert calculate("sqrt(9)") == "3"
