"""Safe integer expression engine for Programmer mode.

Values are stored as unsigned bit patterns and normalized to the selected word
size after every operation. In signed mode, the same pattern is interpreted as
two's-complement for decimal display and right shifts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, IntEnum

from .errors import (
    CalculatorSyntaxError,
    InvalidProgrammerNumberError,
    ProgrammerDivisionByZeroError,
    ProgrammerError,
    ProgrammerShiftError,
)


class NumberBase(str, Enum):
    BIN = "BIN"
    OCT = "OCT"
    DEC = "DEC"
    HEX = "HEX"

    @property
    def radix(self) -> int:
        return {
            NumberBase.BIN: 2,
            NumberBase.OCT: 8,
            NumberBase.DEC: 10,
            NumberBase.HEX: 16,
        }[self]


class WordSize(IntEnum):
    BITS_8 = 8
    BITS_16 = 16
    BITS_32 = 32
    BITS_64 = 64


class Signedness(str, Enum):
    UNSIGNED = "UNSIGNED"
    SIGNED = "SIGNED"


@dataclass(frozen=True)
class _Token:
    kind: str
    value: str
    position: int


_OPERATOR_WORDS = {"AND": "&", "OR": "|", "XOR": "^", "NOT": "~"}
_SYMBOLS = {
    "&": "&",
    "|": "|",
    "^": "^",
    "~": "~",
    "+": "+",
    "-": "-",
    "*": "*",
    "/": "/",
    "(": "(",
    ")": ")",
}


def _tokenize(expression: str) -> list[_Token]:
    tokens: list[_Token] = []
    position = 0
    while position < len(expression):
        char = expression[position]
        if char.isspace():
            position += 1
            continue
        if expression.startswith("<<", position):
            tokens.append(_Token("OP", "<<", position))
            position += 2
            continue
        if expression.startswith(">>", position):
            tokens.append(_Token("OP", ">>", position))
            position += 2
            continue
        if char in _SYMBOLS:
            tokens.append(_Token("OP", _SYMBOLS[char], position))
            position += 1
            continue
        if char.isalnum() or char == "_":
            start = position
            while position < len(expression) and (
                expression[position].isalnum() or expression[position] == "_"
            ):
                position += 1
            word = expression[start:position].upper()
            if word in _OPERATOR_WORDS:
                tokens.append(_Token("OP", _OPERATOR_WORDS[word], start))
            else:
                tokens.append(_Token("NUMBER", expression[start:position], start))
            continue
        raise CalculatorSyntaxError(
            f"Invalid programmer character '{char}'", position=position
        )
    tokens.append(_Token("EOF", "", len(expression)))
    return tokens


class _ExpressionParser:
    def __init__(self, tokens: list[_Token], calculator: ProgrammerCalculator):
        self.tokens = tokens
        self.position = 0
        self.calculator = calculator

    def current(self) -> _Token:
        return self.tokens[self.position]

    def consume(self, value: str | None = None) -> _Token:
        token = self.current()
        if value is not None and token.value != value:
            raise CalculatorSyntaxError(
                f"Expected '{value}', got '{token.value}'", position=token.position
            )
        self.position += 1
        return token

    def parse(self) -> int:
        if self.current().kind == "EOF":
            raise CalculatorSyntaxError("Empty programmer expression")
        result = self.parse_or()
        if self.current().kind != "EOF":
            raise CalculatorSyntaxError(
                f"Unexpected token '{self.current().value}'",
                position=self.current().position,
            )
        return result

    def parse_or(self) -> int:
        left = self.parse_xor()
        while self.current().value == "|":
            self.consume("|")
            left = self.calculator._binary("|", left, self.parse_xor())
        return left

    def parse_xor(self) -> int:
        left = self.parse_and()
        while self.current().value == "^":
            self.consume("^")
            left = self.calculator._binary("^", left, self.parse_and())
        return left

    def parse_and(self) -> int:
        left = self.parse_shift()
        while self.current().value == "&":
            self.consume("&")
            left = self.calculator._binary("&", left, self.parse_shift())
        return left

    def parse_shift(self) -> int:
        left = self.parse_additive()
        while self.current().value in ("<<", ">>"):
            operator = self.consume().value
            if (
                self.current().value == "-"
                and self.position + 1 < len(self.tokens)
                and self.tokens[self.position + 1].kind == "NUMBER"
            ):
                self.consume("-")
                right = -self.calculator.parse_value(
                    self.consume().value, self.calculator.base
                )
            else:
                right = self.parse_additive()
            left = self.calculator._binary(operator, left, right)
        return left

    def parse_additive(self) -> int:
        left = self.parse_multiplicative()
        while self.current().value in ("+", "-"):
            operator = self.consume().value
            left = self.calculator._binary(operator, left, self.parse_multiplicative())
        return left

    def parse_multiplicative(self) -> int:
        left = self.parse_unary()
        while self.current().value in ("*", "/"):
            operator = self.consume().value
            left = self.calculator._binary(operator, left, self.parse_unary())
        return left

    def parse_unary(self) -> int:
        if (
            self.current().value == "-"
            and self.position + 1 < len(self.tokens)
            and self.tokens[self.position + 1].kind == "NUMBER"
        ):
            self.consume("-")
            return self.calculator.parse_value("-" + self.consume().value)
        if self.current().value in ("+", "-", "~"):
            operator = self.consume().value
            return self.calculator._unary(operator, self.parse_unary())
        return self.parse_primary()

    def parse_primary(self) -> int:
        token = self.current()
        if token.kind == "NUMBER":
            self.consume()
            return self.calculator.parse_value(token.value)
        if token.value == "(":
            self.consume("(")
            value = self.parse_or()
            if self.current().value != ")":
                raise CalculatorSyntaxError("Missing closing parenthesis ')'")
            self.consume(")")
            return value
        raise CalculatorSyntaxError(
            f"Unexpected token '{token.value}'", position=token.position
        )


class ProgrammerCalculator:
    """Evaluate integer expressions under a base, width, and signedness."""

    def __init__(
        self,
        base: NumberBase | str = NumberBase.DEC,
        word_size: WordSize | int = WordSize.BITS_32,
        signed: bool | Signedness = False,
    ):
        self.base = self._coerce_base(base)
        self.word_size = WordSize(word_size)
        self.signed = (
            signed == Signedness.SIGNED
            if isinstance(signed, Signedness)
            else bool(signed)
        )

    @staticmethod
    def _coerce_base(base: NumberBase | str) -> NumberBase:
        return base if isinstance(base, NumberBase) else NumberBase(str(base).upper())

    @property
    def mask(self) -> int:
        return (1 << int(self.word_size)) - 1

    @property
    def sign_bit(self) -> int:
        return 1 << (int(self.word_size) - 1)

    def _normalize(self, value: int) -> int:
        return value & self.mask

    def to_signed(self, value: int) -> int:
        raw = self._normalize(value)
        return raw - (1 << int(self.word_size)) if raw & self.sign_bit else raw

    def parse_value(self, value: str, base: NumberBase | str | None = None) -> int:
        selected_base = self.base if base is None else self._coerce_base(base)
        text = value.strip()
        if not text:
            raise InvalidProgrammerNumberError("Programmer value cannot be empty")
        sign = 1
        if text[0] in "+-":
            if text[0] == "-":
                sign = -1
            text = text[1:]
        if not text:
            raise InvalidProgrammerNumberError("Programmer value requires digits")
        valid_digits = {
            NumberBase.BIN: "01",
            NumberBase.OCT: "01234567",
            NumberBase.DEC: "0123456789",
            NumberBase.HEX: "0123456789ABCDEFabcdef",
        }[selected_base]
        if any(char not in valid_digits for char in text):
            raise InvalidProgrammerNumberError(
                f"Invalid {selected_base.value} value '{value}'"
            )
        parsed = sign * int(text, selected_base.radix)
        if self.signed:
            minimum = -(1 << (int(self.word_size) - 1))
            maximum = (1 << (int(self.word_size) - 1)) - 1
        else:
            minimum = 0
            maximum = self.mask
        if parsed < minimum or parsed > maximum:
            mode = "signed" if self.signed else "unsigned"
            raise InvalidProgrammerNumberError(
                f"Value {value} is outside the {mode} {self.word_size}-bit range"
            )
        return self._normalize(parsed)

    def evaluate_raw(self, expression: str) -> int:
        return _ExpressionParser(_tokenize(expression), self).parse()

    def evaluate(self, expression: str) -> int:
        raw = self.evaluate_raw(expression)
        return self.to_signed(raw) if self.signed else raw

    def format_value(self, value: int, base: NumberBase | str | None = None) -> str:
        selected_base = self.base if base is None else self._coerce_base(base)
        numeric = self.to_signed(value) if self.signed else self._normalize(value)
        if numeric < 0:
            return "-" + self._format_unsigned(-numeric, selected_base)
        return self._format_unsigned(numeric, selected_base)

    @staticmethod
    def _format_unsigned(value: int, base: NumberBase) -> str:
        return format(
            value,
            {
                NumberBase.BIN: "b",
                NumberBase.OCT: "o",
                NumberBase.DEC: "d",
                NumberBase.HEX: "X",
            }[base],
        )

    def convert(
        self, value: str, base: NumberBase | str | None = None
    ) -> dict[NumberBase, str]:
        raw = self.parse_value(value, base)
        return {selected: self.format_value(raw, selected) for selected in NumberBase}

    def _unary(self, operator: str, value: int) -> int:
        if operator == "+":
            return self._normalize(value)
        if operator == "-":
            if not self.signed:
                raise InvalidProgrammerNumberError(
                    "Negative values require signed mode"
                )
            return self._normalize(-value)
        if operator == "~":
            return self._normalize(~value)
        raise ProgrammerError(f"Unsupported unary operator '{operator}'")

    def _binary(self, operator: str, left: int, right: int) -> int:
        if operator == "+":
            return self._normalize(left + right)
        if operator == "-":
            return self._normalize(left - right)
        if operator == "*":
            return self._normalize(left * right)
        if operator == "/":
            if right == 0:
                raise ProgrammerDivisionByZeroError("Programmer division by zero")
            left_number = self.to_signed(left) if self.signed else left
            right_number = self.to_signed(right) if self.signed else right
            quotient = abs(left_number) // abs(right_number)
            if (left_number < 0) != (right_number < 0):
                quotient = -quotient
            return self._normalize(quotient)
        if operator == "&":
            return self._normalize(left & right)
        if operator == "|":
            return self._normalize(left | right)
        if operator == "^":
            return self._normalize(left ^ right)
        if operator in ("<<", ">>"):
            shift = self.to_signed(right) if self.signed else right
            if shift < 0 or shift >= int(self.word_size):
                raise ProgrammerShiftError(
                    f"Shift count must be between 0 and {int(self.word_size) - 1}"
                )
            if operator == ">>" and self.signed:
                return self._normalize(self.to_signed(left) >> shift)
            if operator == "<<":
                return self._normalize(left << shift)
            return self._normalize(left >> shift)
        raise ProgrammerError(f"Unsupported binary operator '{operator}'")

    def bit_string(self, value: int) -> str:
        raw = self._normalize(value)
        return format(raw, f"0{int(self.word_size)}b")
