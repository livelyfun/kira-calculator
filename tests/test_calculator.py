"""Comprehensive test suite for Kira Calculator Expression Engine."""

import math

from src.calculator.errors import (
    CalculatorDomainError,
    CalculatorOverflowError,
    CalculatorSyntaxError,
    DivisionByZeroError,
    UnknownFunctionError,
)
from src.calculator.evaluator import AngleMode, Evaluator
from src.calculator.logic import calculate, evaluate_expression
from src.calculator.parser import Parser
from src.calculator.tokenizer import tokenize

# ==========================================
# 1. Basic Arithmetic & Precedence
# ==========================================


def test_basic_addition():
    assert calculate("2 + 3") == "5"


def test_basic_subtraction():
    assert calculate("10 - 4") == "6"


def test_basic_multiplication():
    assert calculate("5 * 6") == "30"
    assert calculate("5 × 6") == "30"


def test_basic_division():
    assert calculate("20 / 4") == "5"
    assert calculate("20 ÷ 4") == "5"


def test_operator_precedence():
    assert calculate("2 + 3 × 4") == "14"
    assert calculate("10 - 2 × 3") == "4"
    assert calculate("20 - 10 ÷ 2") == "15"


def test_parentheses():
    assert calculate("(2 + 3) × 4") == "20"
    assert calculate("2 × (3 + 4)") == "14"
    assert calculate("((2 + 3) × (4 + 1))") == "25"


# ==========================================
# 2. Power & Associativity
# ==========================================


def test_power_basic():
    assert calculate("2 ^ 3") == "8"
    assert calculate("3 ^ 2") == "9"


def test_power_right_associativity():
    # 2 ^ 3 ^ 2 == 2 ^ (3 ^ 2) == 2 ^ 9 == 512
    assert calculate("2 ^ 3 ^ 2") == "512"


def test_power_with_parentheses():
    # (2 ^ 3) ^ 2 == 8 ^ 2 == 64
    assert calculate("(2 ^ 3) ^ 2") == "64"


# ==========================================
# 3. Decimals & Scientific Notation
# ==========================================


def test_decimal_arithmetic():
    assert calculate("2.5 × 4") == "10"
    assert calculate("0.1 + 0.2") == "0.3"
    assert calculate("1.25 + 2.75") == "4"


def test_scientific_notation():
    assert calculate("1e5") == "100000"
    assert calculate("2.5e3") == "2500"
    assert calculate("1e-3") == "0.001"
    assert calculate("1e5 × 1e-3") == "100"


# ==========================================
# 4. Negative Numbers & Unary Operators
# ==========================================


def test_negative_numbers():
    assert calculate("-5 + 2") == "-3"
    assert calculate("2 + -5") == "-3"
    assert calculate("-5 × -2") == "10"
    assert calculate("5 - -2") == "7"


def test_multiple_unary_signs():
    assert calculate("--5") == "5"
    assert calculate("---5") == "-5"
    assert calculate("-(-5)") == "5"


def test_unary_with_expressions():
    assert calculate("-(2 + 3)") == "-5"
    assert calculate("-(2 + 3) × 4") == "-20"


# ==========================================
# 5. Implicit Multiplication
# ==========================================


def test_implicit_multiplication_with_parentheses():
    assert calculate("2(3)") == "6"
    assert calculate("(2 + 3)(4 + 1)") == "25"
    assert calculate("3(2 + 4)") == "18"


def test_implicit_multiplication_with_constants():
    res = float(calculate("2π"))
    assert math.isclose(res, 2 * math.pi, rel_tol=1e-11)

    res_e = float(calculate("3e"))
    assert math.isclose(res_e, 3 * math.e, rel_tol=1e-11)


def test_implicit_multiplication_with_functions():
    assert calculate("2sin(90)") == "2"
    assert calculate("3sqrt(16)") == "12"


# ==========================================
# 6. Postfix Operators: Factorial (!) & Percent (%)
# ==========================================


def test_factorial():
    assert calculate("0!") == "1"
    assert calculate("1!") == "1"
    assert calculate("5!") == "120"
    assert calculate("factorial(5)") == "120"
    assert calculate("3! + 4!") == "30"


def test_percent():
    assert calculate("5%") == "0.05"
    assert calculate("100 × 15%") == "15"
    assert calculate("200 × 20%") == "40"


# ==========================================
# 7. Constants
# ==========================================


def test_pi_constant():
    res1 = float(calculate("π"))
    res2 = float(calculate("pi"))
    assert math.isclose(res1, math.pi, rel_tol=1e-12)
    assert math.isclose(res2, math.pi, rel_tol=1e-12)


def test_e_constant():
    res = float(calculate("e"))
    assert math.isclose(res, math.e, rel_tol=1e-12)


def test_phi_constant():
    phi = (1 + math.sqrt(5)) / 2
    res1 = float(calculate("φ"))
    res2 = float(calculate("phi"))
    assert math.isclose(res1, phi, rel_tol=1e-12)
    assert math.isclose(res2, phi, rel_tol=1e-12)


# ==========================================
# 8. Scientific Functions
# ==========================================


def test_square_root():
    assert calculate("sqrt(25)") == "5"
    assert calculate("sqrt(144)") == "12"
    assert calculate("√25") == "5"
    assert calculate("√(144)") == "12"


def test_logarithms():
    assert calculate("log(100)") == "2"
    assert calculate("log(1000)") == "3"
    assert calculate("ln(e)") == "1"


def test_exp_and_abs():
    assert calculate("exp(0)") == "1"
    assert calculate("abs(-42)") == "42"
    assert calculate("abs(42)") == "42"


def test_hyperbolic_functions():
    assert calculate("sinh(0)") == "0"
    assert calculate("cosh(0)") == "1"
    assert calculate("tanh(0)") == "0"


# ==========================================
# 9. Trigonometry & Angle Modes
# ==========================================


def test_trig_degrees_exact():
    assert calculate("sin(0)") == "0"
    assert calculate("sin(90)") == "1"
    assert calculate("sin(180)") == "0"
    assert calculate("sin(270)") == "-1"
    assert calculate("sin(360)") == "0"

    assert calculate("cos(0)") == "1"
    assert calculate("cos(90)") == "0"
    assert calculate("cos(180)") == "-1"
    assert calculate("cos(270)") == "0"

    assert calculate("tan(0)") == "0"
    assert calculate("tan(45)") == "1"
    assert calculate("tan(135)") == "-1"
    assert calculate("cos(60)") == "0.5"


def test_trig_radians():
    assert math.isclose(float(calculate("sin(pi / 2)", "RAD")), 1.0, rel_tol=1e-11)
    assert math.isclose(float(calculate("cos(pi)", "RAD")), -1.0, rel_tol=1e-11)
    assert math.isclose(float(calculate("tan(pi / 4)", "RAD")), 1.0, rel_tol=1e-11)


def test_inverse_trig():
    assert calculate("asin(1)", "DEG") == "90"
    assert calculate("acos(1)", "DEG") == "0"
    assert calculate("atan(1)", "DEG") == "45"

    assert math.isclose(float(calculate("asin(1)", "RAD")), math.pi / 2, rel_tol=1e-11)
    assert math.isclose(float(calculate("atan(1)", "RAD")), math.pi / 4, rel_tol=1e-11)


def test_grad_angle_mode():
    assert calculate("sin(100)", "GRAD") == "1"
    assert calculate("cos(200)", "GRAD") == "-1"
    assert calculate("tan(50)", "GRAD") == "1"


# ==========================================
# 10. Error Handling & Specific Exception Types
# ==========================================


def test_division_by_zero_error():
    res = evaluate_expression("10 ÷ 0")
    assert not res.success
    assert isinstance(res.error, DivisionByZeroError)
    assert "Division by zero" in res.formatted_value


def test_tan_singularity_domain_error():
    res = evaluate_expression("tan(90)", angle_mode="DEG")
    assert not res.success
    assert isinstance(res.error, CalculatorDomainError)
    assert "undefined" in res.formatted_value.lower()


def test_negative_square_root_domain_error():
    res = evaluate_expression("sqrt(-1)")
    assert not res.success
    assert isinstance(res.error, CalculatorDomainError)
    assert "negative" in res.formatted_value.lower()


def test_log_domain_error():
    res1 = evaluate_expression("log(0)")
    res2 = evaluate_expression("log(-5)")
    res3 = evaluate_expression("ln(0)")
    assert not res1.success and isinstance(res1.error, CalculatorDomainError)
    assert not res2.success and isinstance(res2.error, CalculatorDomainError)
    assert not res3.success and isinstance(res3.error, CalculatorDomainError)


def test_invalid_syntax_error():
    res1 = evaluate_expression("2 +")
    res2 = evaluate_expression("((2 + 3)")
    res3 = evaluate_expression("2 + 3)")
    res4 = evaluate_expression("()")
    res5 = evaluate_expression("")

    assert not res1.success and isinstance(res1.error, CalculatorSyntaxError)
    assert not res2.success and isinstance(res2.error, CalculatorSyntaxError)
    assert not res3.success and isinstance(res3.error, CalculatorSyntaxError)
    assert not res4.success and isinstance(res4.error, CalculatorSyntaxError)
    assert not res5.success and isinstance(res5.error, CalculatorSyntaxError)


def test_unknown_function_error():
    res = evaluate_expression("unknownfunc(5)")
    assert not res.success
    assert isinstance(res.error, UnknownFunctionError)


def test_overflow_error():
    res1 = evaluate_expression("171!")
    res2 = evaluate_expression("10 ^ 1000000")
    assert not res1.success and isinstance(res1.error, CalculatorOverflowError)
    assert not res2.success and isinstance(res2.error, CalculatorOverflowError)


# ==========================================
# 11. AST & Direct Evaluator Tests
# ==========================================


def test_ast_evaluation_direct():
    tokens = tokenize("2 + 3 * 4")
    parser = Parser(tokens)
    ast = parser.parse()
    evaluator = Evaluator(angle_mode=AngleMode.DEG)
    assert evaluator.evaluate(ast) == 14.0
