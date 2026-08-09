import math

from .tokenizer import Token


class Parser:

    def __init__(self, tokens, angle_mode="DEG"):
        self.tokens = tokens
        self.position = 0
        self.angle_mode = angle_mode

    def parse(self):
        if not self.tokens:
            raise ValueError("Empty expression")

        result = self.parse_expression()

        if self.position < len(self.tokens):
            token = self.current_token()

            raise ValueError(
                f"Unexpected token: {token.value}"
            )

        return result

    # ==========================================
    # Token helpers
    # ==========================================

    def current_token(self):
        if self.position >= len(self.tokens):
            return None

        return self.tokens[self.position]

    def consume(self, token_type=None):

        token = self.current_token()

        if token is None:
            raise ValueError("Unexpected end of expression")

        if token_type is not None and token.type != token_type:
            raise ValueError(
                f"Expected {token_type}, got {token.type}"
            )

        self.position += 1

        return token

    # ==========================================
    # Expression
    # ==========================================

    def parse_expression(self):

        result = self.parse_term()

        while True:

            token = self.current_token()

            if token is None:
                break

            if token.type == "PLUS":
                self.consume()
                result += self.parse_term()

            elif token.type == "MINUS":
                self.consume()
                result -= self.parse_term()

            else:
                break

        return result

    # ==========================================
    # Multiplication / Division
    # ==========================================

    def parse_term(self):

        result = self.parse_power()

        while True:

            token = self.current_token()

            if token is None:
                break

            if token.type == "MULTIPLY":
                self.consume()
                result *= self.parse_power()

            elif token.type == "DIVIDE":
                self.consume()

                divisor = self.parse_power()

                if divisor == 0:
                    raise ZeroDivisionError(
                        "Division by zero"
                    )

                result /= divisor

            else:
                break

        return result

    # ==========================================
    # Powers
    # ==========================================

    def parse_power(self):

        result = self.parse_unary()

        token = self.current_token()

        if token is not None and token.type == "POWER":

            self.consume()

            exponent = self.parse_power()

            result = result ** exponent

        return result

    # ==========================================
    # Unary + / -
    # ==========================================

    def parse_unary(self):

        token = self.current_token()

        if token is not None:

            if token.type == "PLUS":
                self.consume()
                return self.parse_unary()

            if token.type == "MINUS":
                self.consume()
                return -self.parse_unary()

        return self.parse_postfix()

    # ==========================================
    # Percentage
    # ==========================================

    def parse_postfix(self):

        result = self.parse_primary()

        while True:

            token = self.current_token()

            if token is None:
                break

            if token.type == "PERCENT":

                self.consume()

                result /= 100

            else:
                break

        return result

    # ==========================================
    # Numbers / functions / constants /
    # parentheses
    # ==========================================

    def parse_primary(self):

        token = self.current_token()

        if token is None:
            raise ValueError(
                "Expected expression"
            )

        # Number
        if token.type == "NUMBER":

            self.consume()

            return float(token.value)

        # Constant
        if token.type == "CONSTANT":

            self.consume()

            if token.value == "pi":
                return math.pi

            if token.value == "e":
                return math.e

            raise ValueError(
                f"Unknown constant: {token.value}"
            )

        # Function
        if token.type == "FUNCTION":

            function_name = self.consume().value

            self.consume("LPAREN")

            argument = self.parse_expression()

            self.consume("RPAREN")

            return self.apply_function(
                function_name,
                argument,
            )

        # Parentheses
        if token.type == "LPAREN":

            self.consume()

            result = self.parse_expression()

            self.consume("RPAREN")

            return result

        raise ValueError(
            f"Unexpected token: {token.value}"
        )

    # ==========================================
    # Scientific functions
    # ==========================================

    def apply_function(self, name, value):

        if name in {"sin", "cos", "tan"}:

            angle = value

            if self.angle_mode == "DEG":
                angle = math.radians(angle)

            if name == "sin":
                return math.sin(angle)

            if name == "cos":
                return math.cos(angle)

            if name == "tan":
                return math.tan(angle)

        if name == "sqrt":

            if value < 0:
                raise ValueError(
                    "Square root of negative number"
                )

            return math.sqrt(value)

        if name == "log":

            if value <= 0:
                raise ValueError(
                    "Logarithm domain error"
                )

            return math.log10(value)

        if name == "ln":

            if value <= 0:
                raise ValueError(
                    "Natural logarithm domain error"
                )

            return math.log(value)

        raise ValueError(
            f"Unknown function: {name}"
        )