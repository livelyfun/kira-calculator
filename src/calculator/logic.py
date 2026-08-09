import math

from .parser import Parser
from .tokenizer import tokenize


def calculate(expression: str):
    try:
        tokens = tokenize(expression)

        parser = Parser(tokens)

        result = parser.parse()

        result = round(result, 12)
        
        if result == int(result):
            result = int(result)

        return str(result)

    except (ValueError, ZeroDivisionError):
        return "Error"