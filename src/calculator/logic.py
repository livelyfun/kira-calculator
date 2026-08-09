from .parser import Parser
from .tokenizer import tokenize


def calculate(expression: str):
    try:
        tokens = tokenize(expression)

        parser = Parser(tokens)

        result = parser.parse()

        if result == int(result):
            return str(int(result))

        return str(result)

    except (ValueError, ZeroDivisionError):
        return "Error"