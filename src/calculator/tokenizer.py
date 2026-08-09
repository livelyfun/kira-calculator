from dataclasses import dataclass


@dataclass
class Token:
    type: str
    value: str


OPERATORS = {
    "+": "PLUS",
    "-": "MINUS",
    "×": "MULTIPLY",
    "*": "MULTIPLY",
    "÷": "DIVIDE",
    "/": "DIVIDE",
    "^": "POWER",
    "%": "PERCENT",
    "(": "LPAREN",
    ")": "RPAREN",
}

FUNCTIONS = {
    "sin",
    "cos",
    "tan",
    "log",
    "ln",
    "sqrt",
}

CONSTANTS = {
    "pi",
    "π",
    "e",
}


def tokenize(expression: str):
    tokens = []
    position = 0

    while position < len(expression):

        char = expression[position]

        # Ignore whitespace
        if char.isspace():
            position += 1
            continue

        # Numbers
        if char.isdigit() or char == ".":
            start = position
            decimal_count = 0

            while position < len(expression):
                current = expression[position]

                if current == ".":
                    decimal_count += 1

                    if decimal_count > 1:
                        raise ValueError("Invalid number")

                elif not current.isdigit():
                    break

                position += 1

            value = expression[start:position]

            if value == ".":
                raise ValueError("Invalid number")

            tokens.append(Token("NUMBER", value))
            continue

        # Operators and parentheses
        if char in OPERATORS:
            tokens.append(
                Token(
                    OPERATORS[char],
                    char,
                )
            )
            position += 1
            continue

        # Names: functions and constants
        if char.isalpha():
            start = position

            while position < len(expression):
                current = expression[position]

                if not current.isalpha():
                    break

                position += 1

            name = expression[start:position].lower()

            if name in FUNCTIONS:
                tokens.append(Token("FUNCTION", name))

            elif name in CONSTANTS:
                if name == "π":
                    name = "pi"
            
                tokens.append(Token("CONSTANT", name))

            else:
                raise ValueError(
                    f"Unknown name: {name}"
                )

            continue

        raise ValueError(
            f"Invalid character: {char}"
        )

    return tokens