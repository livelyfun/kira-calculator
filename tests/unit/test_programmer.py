"""Unit tests for the Programmer calculation mode."""

import unittest

from kira_calculator.core.errors import (
    InvalidProgrammerNumberError,
    ProgrammerDivisionByZeroError,
    ProgrammerShiftError,
)
from kira_calculator.modes.programmer import (
    NumberBase,
    ProgrammerCalculator,
    Signedness,
    WordSize,
)


class TestProgrammerCalculator(unittest.TestCase):
    def test_decimal_basic_arithmetic(self):
        calc = ProgrammerCalculator(base=NumberBase.DEC, word_size=WordSize.BITS_32)
        self.assertEqual(calc.evaluate("10 + 20"), 30)
        self.assertEqual(calc.evaluate("100 - 45"), 55)
        self.assertEqual(calc.evaluate("6 * 7"), 42)
        self.assertEqual(calc.evaluate("100 / 5"), 20)

    def test_hexadecimal_arithmetic(self):
        calc = ProgrammerCalculator(base=NumberBase.HEX, word_size=WordSize.BITS_32)
        self.assertEqual(calc.format_value(calc.evaluate("A + 5")), "F")
        self.assertEqual(calc.format_value(calc.evaluate("10 * 2")), "20")
        self.assertEqual(calc.format_value(calc.evaluate("FF + 1")), "100")

    def test_binary_arithmetic(self):
        calc = ProgrammerCalculator(base=NumberBase.BIN, word_size=WordSize.BITS_8)
        self.assertEqual(calc.format_value(calc.evaluate("1010 + 0101")), "1111")
        self.assertEqual(calc.format_value(calc.evaluate("1100 & 1010")), "1000")
        self.assertEqual(calc.format_value(calc.evaluate("1100 | 1010")), "1110")
        self.assertEqual(calc.format_value(calc.evaluate("1100 ^ 1010")), "110")

    def test_bitwise_shifts(self):
        calc = ProgrammerCalculator(base=NumberBase.DEC, word_size=WordSize.BITS_16)
        self.assertEqual(calc.evaluate("1 << 4"), 16)
        self.assertEqual(calc.evaluate("64 >> 2"), 16)

    def test_shift_out_of_bounds(self):
        calc = ProgrammerCalculator(base=NumberBase.DEC, word_size=WordSize.BITS_16)
        with self.assertRaises(ProgrammerShiftError):
            calc.evaluate("1 << 16")
        with self.assertRaises(ProgrammerShiftError):
            calc.evaluate("1 << -1")

    def test_division_by_zero(self):
        calc = ProgrammerCalculator(base=NumberBase.DEC)
        with self.assertRaises(ProgrammerDivisionByZeroError):
            calc.evaluate("10 / 0")

    def test_signed_twos_complement_8bit(self):
        calc = ProgrammerCalculator(
            base=NumberBase.DEC,
            word_size=WordSize.BITS_8,
            signed=Signedness.SIGNED,
        )
        self.assertEqual(calc.to_signed(0xFF), -1)
        self.assertEqual(calc.to_signed(0x80), -128)
        self.assertEqual(calc.to_signed(0x7F), 127)
        self.assertEqual(calc.evaluate("5 - 10"), -5)

    def test_unsigned_wrap_around_8bit(self):
        calc = ProgrammerCalculator(
            base=NumberBase.DEC,
            word_size=WordSize.BITS_8,
            signed=Signedness.UNSIGNED,
        )
        # 255 + 1 wraps to 0 in 8-bit unsigned
        self.assertEqual(calc.evaluate("255 + 1"), 0)

    def test_multi_base_conversion(self):
        calc = ProgrammerCalculator(base=NumberBase.DEC, word_size=WordSize.BITS_16)
        conversions = calc.convert("255")
        self.assertEqual(conversions[NumberBase.DEC], "255")
        self.assertEqual(conversions[NumberBase.HEX], "FF")
        self.assertEqual(conversions[NumberBase.BIN], "11111111")
        self.assertEqual(conversions[NumberBase.OCT], "377")

    def test_bit_string(self):
        calc = ProgrammerCalculator(base=NumberBase.DEC, word_size=WordSize.BITS_8)
        self.assertEqual(calc.bit_string(5), "00000101")
        self.assertEqual(calc.bit_string(255), "11111111")

    def test_invalid_radix_digits(self):
        calc_bin = ProgrammerCalculator(base=NumberBase.BIN)
        with self.assertRaises(InvalidProgrammerNumberError):
            calc_bin.parse_value("102")


if __name__ == "__main__":
    unittest.main()
