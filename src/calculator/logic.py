import math

from .parser import Parser
from .tokenizer import tokenize


def calculate(expression: str, angle_mode="DEG"):
    try:
        tokens = tokenize(expression)

        parser = Parser(tokens, angle_mode=angle_mode)

        result = parser.parse()

        result = round(result, 12)
        
        if result == int(result):
            result = int(result)

        return str(result)

    except (ValueError, ZeroDivisionError):
        return "Error"