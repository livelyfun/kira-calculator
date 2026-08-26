"""Recursive-descent Parser for mathematical expressions generating an AST."""

from .ast_nodes import (
    ASTNode,
    BinaryOpNode,
    ConstantNode,
    FunctionCallNode,
    NumberNode,
    PostfixOpNode,
    UnaryOpNode,
)
from .errors import CalculatorSyntaxError
from .tokenizer import Token, TokenType


class Parser:
    """Parses a sequence of Tokens into an Abstract Syntax Tree (AST)."""

    MAX_DEPTH = 200

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.position = 0
        self._depth = 0

    def parse(self) -> ASTNode:
        """Parse all tokens into an AST root node.

        Raises:
            CalculatorSyntaxError: If the expression has invalid syntax or is empty.
        """
        if not self.tokens or (
            len(self.tokens) == 1 and self.tokens[0].type == TokenType.EOF
        ):
            raise CalculatorSyntaxError("Empty expression")

        root = self.parse_expression()

        current = self.current_token()
        if current.type != TokenType.EOF:
            if current.type == TokenType.RPAREN:
                raise CalculatorSyntaxError(
                    "Unexpected closing parenthesis ')'", position=current.position
                )
            raise CalculatorSyntaxError(
                f"Unexpected token '{current.value}'", position=current.position
            )

        return root

    # ==========================================
    # Token Navigation Helpers
    # ==========================================

    def current_token(self) -> Token:
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return self.tokens[-1]

    def peek_token(self, offset: int = 1) -> Token:
        idx = self.position + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]

    def consume(self, expected_type: TokenType | None = None) -> Token:
        token = self.current_token()

        if token.type == TokenType.EOF:
            if expected_type == TokenType.RPAREN:
                raise CalculatorSyntaxError(
                    "Missing closing parenthesis ')'", position=token.position
                )
            raise CalculatorSyntaxError(
                "Unexpected end of expression", position=token.position
            )

        if expected_type is not None and token.type != expected_type:
            if expected_type == TokenType.RPAREN:
                raise CalculatorSyntaxError(
                    f"Expected closing parenthesis ')', got '{token.value}'",
                    position=token.position,
                )
            raise CalculatorSyntaxError(
                f"Expected {expected_type.name}, got '{token.value}'",
                position=token.position,
            )

        self.position += 1
        return token

    # ==========================================
    # Grammar Hierarchy
    # ==========================================

    def parse_expression(self) -> ASTNode:
        """Parse binary addition and subtraction: term ((+ | -) term)*"""
        self._depth += 1
        if self._depth > self.MAX_DEPTH:
            raise CalculatorSyntaxError("Expression exceeds maximum nesting depth")

        try:
            left = self.parse_term()

            while True:
                token = self.current_token()
                if token.type == TokenType.PLUS:
                    self.consume(TokenType.PLUS)
                    right = self.parse_term()
                    left = BinaryOpNode(op="+", left=left, right=right)
                elif token.type == TokenType.MINUS:
                    self.consume(TokenType.MINUS)
                    right = self.parse_term()
                    left = BinaryOpNode(op="-", left=left, right=right)
                else:
                    break

            return left
        finally:
            self._depth -= 1

    def parse_term(self) -> ASTNode:
        """Parse multiplication, division, and implicit multiplication."""
        left = self.parse_unary()

        while True:
            token = self.current_token()

            # Explicit multiplication
            if token.type == TokenType.MULTIPLY:
                self.consume(token.type)
                right = self.parse_unary()
                left = BinaryOpNode(op="*", left=left, right=right)

            # Explicit division
            elif token.type == TokenType.DIVIDE:
                self.consume(token.type)
                right = self.parse_unary()
                left = BinaryOpNode(op="/", left=left, right=right)

            # Implicit multiplication (e.g. 2(3), 2pi, (2+3)(4+5), 2sin(30))
            elif self._can_start_implicit_multiplication(token):
                right = self.parse_unary()
                left = BinaryOpNode(op="*", left=left, right=right)

            else:
                break

        return left

    def _can_start_implicit_multiplication(self, token: Token) -> bool:
        """Check if current token can trigger implicit multiplication."""
        return token.type in (
            TokenType.LPAREN,
            TokenType.FUNCTION,
            TokenType.CONSTANT,
        )

    def parse_unary(self) -> ASTNode:
        """Parse prefix unary operators (+ and -)."""
        token = self.current_token()

        if token.type == TokenType.PLUS:
            self.consume(TokenType.PLUS)
            operand = self.parse_unary()
            return UnaryOpNode(op="+", operand=operand)

        if token.type == TokenType.MINUS:
            self.consume(TokenType.MINUS)
            operand = self.parse_unary()
            return UnaryOpNode(op="-", operand=operand)

        return self.parse_power()

    def parse_power(self) -> ASTNode:
        """Parse right-associative power operator: postfix (^ unary)?"""
        left = self.parse_postfix()

        token = self.current_token()
        if token.type == TokenType.POWER:
            self.consume(TokenType.POWER)
            # Power is right-associative and exponent can have unary sign (e.g. 2^-2, 2^3^2)
            right = self.parse_unary()
            return BinaryOpNode(op="^", left=left, right=right)

        return left

    def parse_postfix(self) -> ASTNode:
        """Parse postfix operators such as factorial (!) and percentage (%)."""
        node = self.parse_primary()

        while True:
            token = self.current_token()
            if token.type == TokenType.FACTORIAL:
                self.consume(TokenType.FACTORIAL)
                node = PostfixOpNode(op="!", operand=node)
            elif token.type == TokenType.PERCENT:
                self.consume(TokenType.PERCENT)
                node = PostfixOpNode(op="%", operand=node)
            else:
                break

        return node

    def parse_primary(self) -> ASTNode:
        """Parse primary expressions: numbers, constants, function calls, and parenthesized expressions."""
        token = self.current_token()

        # 1. Number literal
        if token.type == TokenType.NUMBER:
            self.consume(TokenType.NUMBER)
            return NumberNode(value=float(token.value))

        # 2. Constant literal (pi, e, phi)
        if token.type == TokenType.CONSTANT:
            self.consume(TokenType.CONSTANT)
            return ConstantNode(name=token.value)

        # 3. Function call (e.g. sin(90), log(10), sqrt(25))
        if token.type == TokenType.FUNCTION:
            fn_token = self.consume(TokenType.FUNCTION)
            fn_name = fn_token.value

            # If function is followed by parentheses: fn(arg1, arg2, ...)
            if self.current_token().type == TokenType.LPAREN:
                self.consume(TokenType.LPAREN)

                # Check for empty arguments: fn()
                if self.current_token().type == TokenType.RPAREN:
                    raise CalculatorSyntaxError(
                        f"Function '{fn_name}' requires arguments",
                        position=fn_token.position,
                    )

                args: list[ASTNode] = [self.parse_expression()]

                while self.current_token().type == TokenType.COMMA:
                    self.consume(TokenType.COMMA)
                    args.append(self.parse_expression())

                self.consume(TokenType.RPAREN)
                return FunctionCallNode(name=fn_name, args=args)

            # Allow prefix syntax for sqrt e.g. √25 -> sqrt(25)
            if fn_name == "sqrt":
                arg = self.parse_power()
                return FunctionCallNode(name="sqrt", args=[arg])

            raise CalculatorSyntaxError(
                f"Expected '(' after function '{fn_name}'",
                position=fn_token.position,
            )

        # 4. Parenthesized expression: (expr)
        if token.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)

            if self.current_token().type == TokenType.RPAREN:
                raise CalculatorSyntaxError(
                    "Empty parentheses '()'",
                    position=token.position,
                )

            expr = self.parse_expression()
            self.consume(TokenType.RPAREN)
            return expr

        # 5. Unexpected token or end of input
        if token.type == TokenType.EOF:
            raise CalculatorSyntaxError(
                "Unexpected end of expression", position=token.position
            )

        if token.type == TokenType.RPAREN:
            raise CalculatorSyntaxError(
                "Unexpected closing parenthesis ')'", position=token.position
            )

        raise CalculatorSyntaxError(
            f"Unexpected token '{token.value}'", position=token.position
        )
