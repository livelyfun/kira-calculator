"""Evaluator visitor that interprets the AST and computes numerical results."""

import math
from enum import Enum

from .ast_nodes import (
    ASTNode,
    BinaryOpNode,
    ConstantNode,
    FunctionCallNode,
    NumberNode,
    PostfixOpNode,
    UnaryOpNode,
)
from .errors import (
    CalculatorDomainError,
    CalculatorError,
    CalculatorOverflowError,
    CalculatorSyntaxError,
    DivisionByZeroError,
    UnknownConstantError,
    UnknownFunctionError,
)

PHI = (1 + math.sqrt(5)) / 2  # Golden Ratio ~ 1.618033988749895


class AngleMode(str, Enum):
    """Supported angle measurement modes."""

    DEG = "DEG"
    RAD = "RAD"
    GRAD = "GRAD"


class Evaluator:
    """Evaluates an AST under a specified AngleMode."""

    def __init__(self, angle_mode: AngleMode | str = AngleMode.DEG):
        if isinstance(angle_mode, str):
            angle_mode = AngleMode(angle_mode.upper())
        self.angle_mode = angle_mode

    def evaluate(self, node: ASTNode) -> float:
        """Recursively evaluate an AST node and return its floating-point value."""
        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, ConstantNode):
            return self._eval_constant(node)

        if isinstance(node, UnaryOpNode):
            return self._eval_unary(node)

        if isinstance(node, BinaryOpNode):
            return self._eval_binary(node)

        if isinstance(node, PostfixOpNode):
            return self._eval_postfix(node)

        if isinstance(node, FunctionCallNode):
            return self._eval_function(node)

        raise CalculatorError(f"Unknown AST node type: {type(node).__name__}")

    def _eval_constant(self, node: ConstantNode) -> float:
        if node.name == "pi":
            return math.pi
        if node.name == "e":
            return math.e
        if node.name == "phi":
            return PHI
        raise UnknownConstantError(f"Unknown constant: '{node.name}'")

    def _eval_unary(self, node: UnaryOpNode) -> float:
        val = self.evaluate(node.operand)
        if node.op == "+":
            return +val
        if node.op == "-":
            return -val
        raise CalculatorSyntaxError(f"Unsupported unary operator '{node.op}'")

    def _eval_binary(self, node: BinaryOpNode) -> float:
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)

        if node.op == "+":
            return left + right

        if node.op == "-":
            return left - right

        if node.op in ("*", "×"):
            return left * right

        if node.op in ("/", "÷"):
            if right == 0.0:
                raise DivisionByZeroError("Division by zero")
            return left / right

        if node.op == "^":
            if left == 0.0 and right < 0:
                raise DivisionByZeroError(
                    "Division by zero in power with negative exponent"
                )
            if left < 0.0 and not right.is_integer():
                raise CalculatorDomainError(
                    "Domain error: negative base with non-integer exponent is complex"
                )
            try:
                result = left**right
                if isinstance(result, complex):
                    raise CalculatorDomainError("Domain error: complex result")
                return float(result)
            except OverflowError as err:
                raise CalculatorOverflowError(
                    "Calculation overflow in power operation"
                ) from err

        raise CalculatorSyntaxError(f"Unsupported binary operator '{node.op}'")

    def _eval_postfix(self, node: PostfixOpNode) -> float:
        val = self.evaluate(node.operand)

        if node.op == "%":
            return val / 100.0

        if node.op == "!":
            if val < 0:
                raise CalculatorDomainError("Factorial of negative number is undefined")
            if not math.isclose(val, round(val), abs_tol=1e-9):
                raise CalculatorDomainError("Factorial requires an integer value")
            n = int(round(val))
            if n > 170:
                raise CalculatorOverflowError(
                    f"Factorial of {n} exceeds maximum floating-point representation (n > 170)"
                )
            return float(math.factorial(n))

        raise CalculatorSyntaxError(f"Unsupported postfix operator '{node.op}'")

    def _eval_function(self, node: FunctionCallNode) -> float:
        if not node.args:
            raise CalculatorSyntaxError(f"Function '{node.name}' requires arguments")

        evaluated_args = [self.evaluate(arg) for arg in node.args]
        arg = evaluated_args[0]
        name = node.name.lower()

        # Trigonometric functions
        if name == "sin":
            return self._sin(arg)
        if name == "cos":
            return self._cos(arg)
        if name == "tan":
            return self._tan(arg)

        # Inverse trigonometric functions
        if name == "asin":
            return self._asin(arg)
        if name == "acos":
            return self._acos(arg)
        if name == "atan":
            return self._atan(arg)

        # Hyperbolic functions
        if name == "sinh":
            try:
                return math.sinh(arg)
            except OverflowError as err:
                raise CalculatorOverflowError("sinh result overflow") from err
        if name == "cosh":
            try:
                return math.cosh(arg)
            except OverflowError as err:
                raise CalculatorOverflowError("cosh result overflow") from err
        if name == "tanh":
            return math.tanh(arg)

        # Roots, logs, exp, abs
        if name == "sqrt":
            if arg < 0:
                raise CalculatorDomainError(
                    "Square root of negative number is undefined"
                )
            return math.sqrt(arg)

        if name == "log":
            if arg <= 0:
                raise CalculatorDomainError(
                    "Logarithm of non-positive number is undefined"
                )
            return math.log10(arg)

        if name == "ln":
            if arg <= 0:
                raise CalculatorDomainError(
                    "Natural logarithm of non-positive number is undefined"
                )
            return math.log(arg)

        if name == "exp":
            try:
                return math.exp(arg)
            except OverflowError as err:
                raise CalculatorOverflowError("exp result overflow") from err

        if name == "abs":
            return abs(arg)

        if name == "factorial":
            if arg < 0:
                raise CalculatorDomainError("Factorial of negative number is undefined")
            if not math.isclose(arg, round(arg), abs_tol=1e-9):
                raise CalculatorDomainError("Factorial requires an integer value")
            n = int(round(arg))
            if n > 170:
                raise CalculatorOverflowError(
                    f"Factorial of {n} exceeds maximum floating-point representation (n > 170)"
                )
            return float(math.factorial(n))

        raise UnknownFunctionError(f"Unknown function '{name}'")

    # ==========================================
    # Trigonometry Helpers
    # ==========================================

    def _sin(self, x: float) -> float:
        if self.angle_mode == AngleMode.DEG:
            norm = x % 360.0
            if (
                math.isclose(norm, 0.0, abs_tol=1e-12)
                or math.isclose(norm, 180.0, abs_tol=1e-12)
                or math.isclose(norm, 360.0, abs_tol=1e-12)
            ):
                return 0.0
            if math.isclose(norm, 90.0, abs_tol=1e-12):
                return 1.0
            if math.isclose(norm, 270.0, abs_tol=1e-12):
                return -1.0
            return math.sin(math.radians(x))

        if self.angle_mode == AngleMode.GRAD:
            norm = x % 400.0
            if math.isclose(norm, 0.0, abs_tol=1e-12) or math.isclose(
                norm, 200.0, abs_tol=1e-12
            ):
                return 0.0
            if math.isclose(norm, 100.0, abs_tol=1e-12):
                return 1.0
            if math.isclose(norm, 300.0, abs_tol=1e-12):
                return -1.0
            return math.sin(x * math.pi / 200.0)

        # RAD
        return math.sin(x)

    def _cos(self, x: float) -> float:
        if self.angle_mode == AngleMode.DEG:
            norm = x % 360.0
            if math.isclose(norm, 90.0, abs_tol=1e-12) or math.isclose(
                norm, 270.0, abs_tol=1e-12
            ):
                return 0.0
            if math.isclose(norm, 0.0, abs_tol=1e-12) or math.isclose(
                norm, 360.0, abs_tol=1e-12
            ):
                return 1.0
            if math.isclose(norm, 180.0, abs_tol=1e-12):
                return -1.0
            return math.cos(math.radians(x))

        if self.angle_mode == AngleMode.GRAD:
            norm = x % 400.0
            if math.isclose(norm, 100.0, abs_tol=1e-12) or math.isclose(
                norm, 300.0, abs_tol=1e-12
            ):
                return 0.0
            if math.isclose(norm, 0.0, abs_tol=1e-12) or math.isclose(
                norm, 400.0, abs_tol=1e-12
            ):
                return 1.0
            if math.isclose(norm, 200.0, abs_tol=1e-12):
                return -1.0
            return math.cos(x * math.pi / 200.0)

        # RAD
        return math.cos(x)

    def _tan(self, x: float) -> float:
        if self.angle_mode == AngleMode.DEG:
            norm = x % 180.0
            if math.isclose(norm, 90.0, abs_tol=1e-9):
                raise CalculatorDomainError("tan is undefined at 90° + 180°k")
            if math.isclose(norm, 0.0, abs_tol=1e-12) or math.isclose(
                norm, 180.0, abs_tol=1e-12
            ):
                return 0.0
            if math.isclose(norm, 45.0, abs_tol=1e-12):
                return 1.0
            if math.isclose(norm, 135.0, abs_tol=1e-12):
                return -1.0
            return math.tan(math.radians(x))

        if self.angle_mode == AngleMode.GRAD:
            norm = x % 200.0
            if math.isclose(norm, 100.0, abs_tol=1e-9):
                raise CalculatorDomainError("tan is undefined at 100 grad + 200 grad*k")
            if math.isclose(norm, 0.0, abs_tol=1e-12) or math.isclose(
                norm, 200.0, abs_tol=1e-12
            ):
                return 0.0
            return math.tan(x * math.pi / 200.0)

        # RAD
        # Check singularity in radians near pi/2 + k*pi
        half_pi = math.pi / 2.0
        norm_rad = (x - half_pi) % math.pi
        if math.isclose(norm_rad, 0.0, abs_tol=1e-12):
            raise CalculatorDomainError("tan is undefined at π/2 + kπ")
        return math.tan(x)

    def _asin(self, x: float) -> float:
        if x < -1.0 or x > 1.0:
            raise CalculatorDomainError("asin argument must be between -1 and 1")
        rad = math.asin(x)
        if self.angle_mode == AngleMode.DEG:
            return math.degrees(rad)
        if self.angle_mode == AngleMode.GRAD:
            return rad * 200.0 / math.pi
        return rad

    def _acos(self, x: float) -> float:
        if x < -1.0 or x > 1.0:
            raise CalculatorDomainError("acos argument must be between -1 and 1")
        rad = math.acos(x)
        if self.angle_mode == AngleMode.DEG:
            return math.degrees(rad)
        if self.angle_mode == AngleMode.GRAD:
            return rad * 200.0 / math.pi
        return rad

    def _atan(self, x: float) -> float:
        rad = math.atan(x)
        if self.angle_mode == AngleMode.DEG:
            return math.degrees(rad)
        if self.angle_mode == AngleMode.GRAD:
            return rad * 200.0 / math.pi
        return rad
