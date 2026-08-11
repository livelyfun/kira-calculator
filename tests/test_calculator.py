import math

from src.calculator.logic import calculate


def test_basic_addition():
    assert calculate("2 + 3") == "5"


def test_operator_precedence():
    assert calculate("2 + 3 × 4") == "14"


def test_parentheses():
    assert calculate("(2 + 3) × 4") == "20"


def test_power():
    assert calculate("2 ^ 3") == "8"


def test_square_root():
    assert calculate("sqrt(25)") == "5"


def test_sine_degrees():
    assert calculate("sin(90)") == "1"


def test_cosine_degrees():
    assert calculate("cos(60)") == "0.5"


def test_tangent_degrees():
    assert calculate("tan(45)") == "1"


def test_logarithm():
    assert calculate("log(100)") == "2"


def test_natural_logarithm():
    assert calculate("ln(e)") == "1"


def test_pi_constant():
    result = float(calculate("π"))

    assert math.isclose(result, math.pi, rel_tol=1e-12)


def test_e_constant():
    result = float(calculate("e"))

    assert math.isclose(result, math.e, rel_tol=1e-12)


def test_combined_expression():
    assert calculate("2 + 3 × sqrt(16)") == "14"


def test_division_by_zero():
    assert calculate("10 ÷ 0") == "Error"


def test_invalid_expression():
    assert calculate("2 +") == "Error"


def test_invalid_square_root():
    assert calculate("sqrt(-1)") == "Error"


def test_invalid_logarithm():
    assert calculate("log(-5)") == "Error"

def test_sine_radians():
    result = float(
        calculate("sin(1.5707963267948966)", "RAD")
    )
    assert abs(result - 1) < 1e-10


def test_cosine_radians():
    result = float(
        calculate("cos(3.141592653589793)", "RAD")
    )
    assert abs(result + 1) < 1e-10


def test_tangent_radians():
    result = float(
        calculate("tan(0.7853981633974483)", "RAD")
    )
    assert abs(result - 1) < 1e-10