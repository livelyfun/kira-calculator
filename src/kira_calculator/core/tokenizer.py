"""Lexer / Tokenizer for mathematical expressions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from .errors import (
    CalculatorSyntaxError,
    InvalidNumberError,
    SecurityError,
    UnknownFunctionError,
)

MAX_EXPRESSION_LENGTH = 2000


class TokenType(Enum):
    """Enumeration of recognized lexical token types."""

    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    PERCENT = auto()
    FACTORIAL = auto()
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    FUNCTION = auto()
    CONSTANT = auto()
    EOF = auto()


@dataclass(frozen=True)
class Token:
    """Represents a lexical token in an expression with position."""

    type: TokenType
    value: str
    position: int


OPERATOR_MAP = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.MULTIPLY,
    "×": TokenType.MULTIPLY,
    "/": TokenType.DIVIDE,
    "÷": TokenType.DIVIDE,
    "%": TokenType.PERCENT,
    "^": TokenType.POWER,
    "!": TokenType.FACTORIAL,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    ",": TokenType.COMMA,
}

KNOWN_FUNCTIONS = {
    "sin",
    "cos",
    "tan",
    "asin",
    "acos",
    "atan",
    "sinh",
    "cosh",
    "tanh",
    "sqrt",
    "cbrt",
    "log",
    "log10",
    "ln",
    "exp",
    "abs",
    "fabs",
    "factorial",
    "ceil",
    "floor",
}

KNOWN_CONSTANTS = {
    "pi": "pi",
    "π": "pi",
    "e": "e",
    "phi": "phi",
    "φ": "phi",
    "tau": "tau",
    "τ": "tau",
}


def tokenize(expression: str) -> list[Token]:
    """Tokenize a mathematical expression string into a list of Tokens.

    Raises:
        SecurityError: If expression exceeds length limits.
        InvalidNumberError: If a numeric literal is malformed.
        UnknownFunctionError: If an unknown function identifier is encountered.
        CalculatorSyntaxError: If an unrecognized character is encountered.
    """
    if len(expression) > MAX_EXPRESSION_LENGTH:
        raise SecurityError(
            f"Expression exceeds maximum allowed length of {MAX_EXPRESSION_LENGTH} characters."
        )

    tokens: list[Token] = []
    position = 0
    length = len(expression)

    while position < length:
        char = expression[position]

        # 1. Skip whitespace
        if char.isspace():
            position += 1
            continue

        # 2. Square root symbol '√'
        if char == "√":
            tokens.append(Token(TokenType.FUNCTION, "sqrt", position))
            position += 1
            continue

        # 3. Greek constants
        if char in ("π", "φ", "τ"):
            tokens.append(Token(TokenType.CONSTANT, KNOWN_CONSTANTS[char], position))
            position += 1
            continue

        # 4. Standard operators and delimiters
        if char in OPERATOR_MAP:
            tokens.append(Token(OPERATOR_MAP[char], char, position))
            position += 1
            continue

        # 5. Numeric literals (including decimal and scientific notation, e.g., 1e-5, 2.5e+10)
        if char.isdigit() or (
            char == "." and position + 1 < length and expression[position + 1].isdigit()
        ):
            start_pos = position
            has_decimal = False

            while position < length and (
                expression[position].isdigit() or expression[position] == "."
            ):
                if expression[position] == ".":
                    if has_decimal:
                        raise InvalidNumberError(
                            "Invalid number: multiple decimal points",
                            position=position,
                        )
                    has_decimal = True
                position += 1

            # Check for scientific notation exponent (e.g. 1e5, 2.5e-3)
            # Only treat 'e' as exponent if followed by optional sign and at least one digit
            if position < length and expression[position].lower() == "e":
                exp_pos = position
                peek = exp_pos + 1
                if peek < length and expression[peek] in ("+", "-"):
                    peek += 1
                if peek < length and expression[peek].isdigit():
                    position = peek
                    while position < length and expression[position].isdigit():
                        position += 1

            num_str = expression[start_pos:position]
            try:
                float(num_str)
            except ValueError as err:
                raise InvalidNumberError(
                    f"Invalid number '{num_str}'", position=start_pos
                ) from err

            tokens.append(Token(TokenType.NUMBER, num_str, start_pos))
            continue

        # 6. Isolated decimal point without digits
        if char == ".":
            raise InvalidNumberError(
                "Invalid number: standalone decimal point", position=position
            )

        # 7. Identifiers (functions and constants)
        if char.isalpha() or char == "_":
            start_pos = position
            while position < length and (
                expression[position].isalnum() or expression[position] == "_"
            ):
                position += 1

            name = expression[start_pos:position].lower()

            if name in KNOWN_FUNCTIONS:
                tokens.append(Token(TokenType.FUNCTION, name, start_pos))
            elif name in KNOWN_CONSTANTS:
                tokens.append(Token(TokenType.CONSTANT, KNOWN_CONSTANTS[name], start_pos))
            else:
                raise UnknownFunctionError(
                    f"Unknown identifier '{name}'", position=start_pos
                )
            continue

        # 8. Unrecognized character
        raise CalculatorSyntaxError(f"Invalid character '{char}'", position=position)

    tokens.append(Token(TokenType.EOF, "", length))
    return tokens

