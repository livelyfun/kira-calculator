"""Comprehensive mathematical calculation engine unit tests."""

import math
import unittest

from kira_calculator.core.engine import calculate, evaluate_expression
from kira_calculator.core.errors import (
    CalculatorDomainError,
    CalculatorOverflowError,
    DivisionByZeroError,
)


class TestEngineBasicArithmetic(unittest.TestCase):
    def test_basic_addition(self):
        self.assertEqual(calculate("2 + 3"), "5")

    def test_basic_subtraction(self):
        self.assertEqual(calculate("10 - 4"), "6")

    def test_basic_multiplication(self):
        self.assertEqual(calculate("5 * 6"), "30")
        self.assertEqual(calculate("5 × 6"), "30")

    def test_basic_division(self):
        self.assertEqual(calculate("20 / 4"), "5")
        self.assertEqual(calculate("20 ÷ 4"), "5")

    def test_operator_precedence(self):
        self.assertEqual(calculate("2 + 3 * 4"), "14")
        self.assertEqual(calculate("2 + 3 × 4"), "14")
        self.assertEqual(calculate("10 - 2 × 3"), "4")
        self.assertEqual(calculate("20 - 10 ÷ 2"), "15")

    def test_parentheses(self):
        self.assertEqual(calculate("(2 + 3) * 4"), "20")
        self.assertEqual(calculate("(2 + 3) × 4"), "20")
        self.assertEqual(calculate("2 * (3 + 4)"), "14")
        self.assertEqual(calculate("((2 + 3) * (4 + 1))"), "25")


class TestEnginePowerAndUnary(unittest.TestCase):
    def test_power_basic(self):
        self.assertEqual(calculate("2 ^ 3"), "8")
        self.assertEqual(calculate("3 ^ 2"), "9")

    def test_power_right_associativity(self):
        # 2 ^ 3 ^ 2 == 2 ^ (3 ^ 2) == 2 ^ 9 == 512
        self.assertEqual(calculate("2 ^ 3 ^ 2"), "512")

    def test_power_with_parentheses(self):
        # (2 ^ 3) ^ 2 == 8 ^ 2 == 64
        self.assertEqual(calculate("(2 ^ 3) ^ 2"), "64")

    def test_unary_minus_precedence(self):
        # In standard math: -2^2 == -(2^2) == -4
        self.assertEqual(calculate("-2^2"), "-4")
        self.assertEqual(calculate("(-2)^2"), "4")
        self.assertEqual(calculate("-(2^2)"), "-4")
        self.assertEqual(calculate("2^-2"), "0.25")
        self.assertEqual(calculate("-2^-2"), "-0.25")

    def test_chained_unary(self):
        self.assertEqual(calculate("--5"), "5")
        self.assertEqual(calculate("---5"), "-5")
        self.assertEqual(calculate("-(-5)"), "5")


class TestEngineScientificNotationAndDecimals(unittest.TestCase):
    def test_decimal_arithmetic(self):
        self.assertEqual(calculate("2.5 × 4"), "10")
        self.assertEqual(calculate("0.1 + 0.2"), "0.3")
        self.assertEqual(calculate("1.25 + 2.75"), "4")
        self.assertEqual(calculate(".5 + .5"), "1")

    def test_scientific_notation(self):
        self.assertEqual(calculate("1e5"), "100000")
        self.assertEqual(calculate("2.5e3"), "2500")
        self.assertEqual(calculate("1e-3"), "0.001")
        self.assertEqual(calculate("1e5 × 1e-3"), "100")
        self.assertEqual(calculate("1.5e+3"), "1500")

    def test_scientific_vs_euler_constant(self):
        # e is Euler constant ~ 2.718281828
        self.assertTrue(math.isclose(float(calculate("e")), math.e, rel_tol=1e-10))
        # 2e is implicit multiplication 2 * e
        self.assertTrue(math.isclose(float(calculate("2e")), 2 * math.e, rel_tol=1e-10))
        # 2e5 is scientific notation 200000
        self.assertEqual(calculate("2e5"), "200000")


class TestEngineImplicitMultiplication(unittest.TestCase):
    def test_implicit_with_parentheses(self):
        self.assertEqual(calculate("2(3)"), "6")
        self.assertEqual(calculate("(2 + 3)(4 + 1)"), "25")
        self.assertEqual(calculate("3(2 + 4)"), "18")

    def test_implicit_with_constants(self):
        res_pi = float(calculate("2pi"))
        self.assertTrue(math.isclose(res_pi, 2 * math.pi, rel_tol=1e-10))

        res_pi_greek = float(calculate("2π"))
        self.assertTrue(math.isclose(res_pi_greek, 2 * math.pi, rel_tol=1e-10))

    def test_implicit_with_functions(self):
        self.assertEqual(calculate("2sin(90)", angle_mode="DEG"), "2")
        self.assertEqual(calculate("3sqrt(16)"), "12")


class TestEngineScientificFunctions(unittest.TestCase):
    def test_trigonometry_deg(self):
        self.assertEqual(calculate("sin(30)", angle_mode="DEG"), "0.5")
        self.assertEqual(calculate("sin(90)", angle_mode="DEG"), "1")
        self.assertEqual(calculate("cos(60)", angle_mode="DEG"), "0.5")
        self.assertEqual(calculate("cos(90)", angle_mode="DEG"), "0")
        self.assertEqual(calculate("tan(45)", angle_mode="DEG"), "1")

    def test_trigonometry_rad(self):
        self.assertTrue(math.isclose(float(calculate("sin(pi / 6)", angle_mode="RAD")), 0.5, abs_tol=1e-10))
        self.assertTrue(math.isclose(float(calculate("cos(pi)", angle_mode="RAD")), -1.0, abs_tol=1e-10))

    def test_trigonometry_grad(self):
        self.assertEqual(calculate("sin(100)", angle_mode="GRAD"), "1")
        self.assertEqual(calculate("cos(200)", angle_mode="GRAD"), "-1")

    def test_inverse_trigonometry(self):
        self.assertEqual(calculate("asin(1)", angle_mode="DEG"), "90")
        self.assertEqual(calculate("acos(1)", angle_mode="DEG"), "0")
        self.assertEqual(calculate("atan(1)", angle_mode="DEG"), "45")

    def test_hyperbolic_functions(self):
        self.assertEqual(calculate("sinh(0)"), "0")
        self.assertEqual(calculate("cosh(0)"), "1")
        self.assertEqual(calculate("tanh(0)"), "0")

    def test_logarithms(self):
        # Per specifications: log(x) is base 10, log10(x) is base 10, ln(x) is natural log
        self.assertEqual(calculate("log(100)"), "2")
        self.assertEqual(calculate("log10(1000)"), "3")
        self.assertEqual(calculate("ln(e)"), "1")

    def test_roots(self):
        self.assertEqual(calculate("sqrt(81)"), "9")
        self.assertEqual(calculate("sqrt(25)"), "5")
        self.assertEqual(calculate("√16"), "4")
        self.assertEqual(calculate("cbrt(27)"), "3")
        self.assertEqual(calculate("cbrt(-8)"), "-2")

    def test_factorials_and_percentages(self):
        self.assertEqual(calculate("5!"), "120")
        self.assertEqual(calculate("0!"), "1")
        self.assertEqual(calculate("factorial(4)"), "24")
        self.assertEqual(calculate("50%"), "0.5")
        self.assertEqual(calculate("200 * 15%"), "30")


class TestEngineErrors(unittest.TestCase):
    def test_division_by_zero(self):
        res = evaluate_expression("10 / 0")
        self.assertFalse(res.success)
        self.assertIsInstance(res.error, DivisionByZeroError)

    def test_tan_singularity(self):
        res = evaluate_expression("tan(90)", angle_mode="DEG")
        self.assertFalse(res.success)
        self.assertIsInstance(res.error, CalculatorDomainError)

    def test_sqrt_negative(self):
        res = evaluate_expression("sqrt(-4)")
        self.assertFalse(res.success)
        self.assertIsInstance(res.error, CalculatorDomainError)

    def test_log_negative_or_zero(self):
        res_zero = evaluate_expression("log(0)")
        res_neg = evaluate_expression("ln(-1)")
        self.assertFalse(res_zero.success)
        self.assertFalse(res_neg.success)

    def test_factorial_overflow(self):
        res = evaluate_expression("171!")
        self.assertFalse(res.success)
        self.assertIsInstance(res.error, CalculatorOverflowError)

    def test_syntax_errors(self):
        self.assertFalse(evaluate_expression("2 +").success)
        self.assertFalse(evaluate_expression("((2 + 3)").success)
        self.assertFalse(evaluate_expression("").success)
        self.assertFalse(evaluate_expression("()").success)


if __name__ == "__main__":
    unittest.main()
