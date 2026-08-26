"""Independent tests for Programmer mode's integer engine."""

import pytest

from src.calculator.errors import (
    CalculatorSyntaxError,
    InvalidProgrammerNumberError,
    ProgrammerDivisionByZeroError,
    ProgrammerShiftError,
)
from src.calculator.programmer import NumberBase, ProgrammerCalculator, Signedness


def test_base_conversion_from_decimal() -> None:
    calculator = ProgrammerCalculator(word_size=16)

    assert calculator.convert("255") == {
        NumberBase.BIN: "11111111",
        NumberBase.OCT: "377",
        NumberBase.DEC: "255",
        NumberBase.HEX: "FF",
    }


@pytest.mark.parametrize(
    ("base", "value", "expected"),
    [
        (NumberBase.BIN, "11111111", 255),
        (NumberBase.OCT, "377", 255),
        (NumberBase.HEX, "FF", 255),
    ],
)
def test_base_conversion_to_decimal(
    base: NumberBase, value: str, expected: int
) -> None:
    calculator = ProgrammerCalculator(base=base, word_size=16)

    assert calculator.evaluate(value) == expected


@pytest.mark.parametrize(
    ("base", "value"),
    [
        (NumberBase.BIN, "102"),
        (NumberBase.OCT, "89"),
        (NumberBase.HEX, "FG"),
        (NumberBase.DEC, "12.5"),
        (NumberBase.DEC, ""),
        (NumberBase.DEC, "-"),
    ],
)
def test_base_specific_validation(base: NumberBase, value: str) -> None:
    calculator = ProgrammerCalculator(base=base, word_size=16)

    with pytest.raises(InvalidProgrammerNumberError):
        calculator.parse_value(value)


def test_integer_arithmetic_and_parentheses() -> None:
    calculator = ProgrammerCalculator(word_size=16)

    assert calculator.evaluate("(2 + 3) * 4") == 20
    assert calculator.evaluate("7 / 2") == 3
    assert calculator.evaluate("10 - 20") == (1 << 16) - 10


@pytest.mark.parametrize(
    ("expression", "expected"),
    [("15 & 6", 6), ("15 | 6", 15), ("15 ^ 6", 9), ("15 AND 6", 6)],
)
def test_bitwise_operations(expression: str, expected: int) -> None:
    assert ProgrammerCalculator(word_size=8).evaluate(expression) == expected


def test_not_respects_word_size() -> None:
    calculator = ProgrammerCalculator(word_size=8)

    assert calculator.evaluate("NOT 0") == 255
    assert calculator.bit_string(calculator.evaluate_raw("~0")) == "11111111"


def test_shifts_and_shift_validation() -> None:
    calculator = ProgrammerCalculator(word_size=8)

    assert calculator.evaluate("1 << 7") == 128
    assert calculator.evaluate("255 >> 1") == 127
    with pytest.raises(ProgrammerShiftError):
        calculator.evaluate("1 << 8")
    with pytest.raises(ProgrammerShiftError):
        calculator.evaluate("1 << -1")


def test_word_size_masks_arithmetic_and_accepts_maximum_unsigned_values() -> None:
    for bits in (8, 16, 32, 64):
        calculator = ProgrammerCalculator(word_size=bits)
        maximum = (1 << bits) - 1
        assert calculator.evaluate(str(maximum)) == maximum
        assert calculator.evaluate("1 - 2") == maximum
        assert calculator.evaluate(f"{maximum} + 1") == 0


def test_signed_twos_complement_display_and_right_shift() -> None:
    calculator = ProgrammerCalculator(word_size=8, signed=Signedness.SIGNED)

    assert calculator.evaluate("-1") == -1
    assert (
        calculator.format_value(calculator.evaluate_raw("-1"), NumberBase.DEC) == "-1"
    )
    assert calculator.evaluate("-4 / 2") == -2
    assert calculator.evaluate("-2 >> 1") == -1
    assert calculator.bit_string(calculator.evaluate_raw("-1")) == "11111111"


def test_signed_range_is_explicit() -> None:
    calculator = ProgrammerCalculator(word_size=8, signed=True)

    assert calculator.evaluate("-128") == -128
    assert calculator.evaluate("127") == 127
    with pytest.raises(InvalidProgrammerNumberError):
        calculator.evaluate("128")

    with pytest.raises(InvalidProgrammerNumberError):
        ProgrammerCalculator(word_size=8).evaluate("-1")


def test_division_by_zero_and_syntax_errors_are_typed() -> None:
    calculator = ProgrammerCalculator()

    with pytest.raises(ProgrammerDivisionByZeroError):
        calculator.evaluate("1 / 0")
    with pytest.raises(CalculatorSyntaxError):
        calculator.evaluate("1 +")
