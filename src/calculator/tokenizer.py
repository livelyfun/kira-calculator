"""Lexer / Tokenizer for mathematical expressions."""

from dataclasses import dataclass
from enum import Enum, auto

from .errors import (
    CalculatorSyntaxError,
    InvalidNumberError,
    UnknownFunctionError,
)


class TokenType(Enum):
    """Enumeration of recognized token types."""

    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
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
    """Represents a lexical token in an expression."""

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
    "^": TokenType.POWER,
    "%": TokenType.PERCENT,
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
    "log",
    "ln",
    "exp",
    "abs",
    "factorial",
}

KNOWN_CONSTANTS = {
    "pi": "pi",
    "π": "pi",
    "e": "e",
    "phi": "phi",
    "φ": "phi",
}


def tokenize(expression: str) -> list[Token]:
    """Tokenize a mathematical expression string into a list of Tokens.

    Raises:
        InvalidNumberError: If a numeric literal is malformed.
        UnknownFunctionError: If an unknown function identifier is found.
        UnknownConstantError: If an unknown identifier is found.
        CalculatorSyntaxError: If an invalid character is encountered.
    """
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

        # 3. Greek constants 'π' and 'φ'
        if char in ("π", "φ"):
            const_name = KNOWN_CONSTANTS[char]
            tokens.append(Token(TokenType.CONSTANT, const_name, position))
            position += 1
            continue

        # 4. Standard operators and delimiters
        if char in OPERATOR_MAP:
            tokens.append(Token(OPERATOR_MAP[char], char, position))
            position += 1
            continue

        # 5. Numeric literals (including decimal and scientific notation e.g. 1e-5, 2.5e+10)
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
                # Validate that Python float can parse the token
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
                tokens.append(
                    Token(TokenType.CONSTANT, KNOWN_CONSTANTS[name], start_pos)
                )
            else:
                raise UnknownFunctionError(
                    f"Unknown function or identifier '{name}'", position=start_pos
                )
            continue

        # 8. Unrecognized character
        raise CalculatorSyntaxError(f"Invalid character '{char}'", position=position)

    tokens.append(Token(TokenType.EOF, "", length))
    return tokens
