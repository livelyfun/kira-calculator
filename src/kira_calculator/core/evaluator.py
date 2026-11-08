"""Evaluator visitor that interprets the AST and computes numerical results safely."""

from __future__ import annotations

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
    CalculatorOverflowError,
    CalculatorSyntaxError,
    DivisionByZeroError,
    SecurityError,
    UnknownConstantError,
    UnknownFunctionError,
)

PHI = (1.0 + math.sqrt(5.0)) / 2.0  # Golden ratio ~ 1.618033988749895
MAX_EXPONENT_ABS = 10000.0


class AngleMode(str, Enum):
    """Supported angle measurement modes."""

    DEG = "DEG"
    RAD = "RAD"
    GRAD = "GRAD"


class Evaluator:
    """Safely evaluates an AST under a specified AngleMode."""

    def __init__(self, angle_mode: AngleMode | str = AngleMode.DEG) -> None:
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

        raise SecurityError(
            f"Unauthorized or unknown AST node encountered: {type(node).__name__}"
        )

    def _eval_constant(self, node: ConstantNode) -> float:
        if node.name == "pi":
            return math.pi
        if node.name == "e":
            return math.e
        if node.name == "phi":
            return PHI
        if node.name == "tau":
            return math.tau
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

        if node.op == "%":
            if right == 0.0:
                raise DivisionByZeroError("Modulo by zero")
            return left % right

        if node.op == "^":
            if left == 0.0 and right < 0:
                raise DivisionByZeroError("Division by zero in power with negative exponent")
            if left < 0.0 and not right.is_integer():
                raise CalculatorDomainError(
                    "Domain error: negative base with non-integer exponent is complex"
                )
            if abs(right) > MAX_EXPONENT_ABS:
                raise CalculatorOverflowError(
                    f"Exponent magnitude exceeds safety threshold ({MAX_EXPONENT_ABS})"
                )
            try:
                result = left**right
                if isinstance(result, complex):
                    raise CalculatorDomainError("Domain error: complex result")
                if math.isinf(result):
                    raise CalculatorOverflowError("Calculation overflow in power operation")
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
        name = node.name.lower()

        # Multi-argument functions
        if name in ("pow", "atan2"):
            if len(node.args) != 2:
                raise CalculatorSyntaxError(f"Function '{name}' requires exactly 2 arguments")
            arg0 = self.evaluate(node.args[0])
            arg1 = self.evaluate(node.args[1])
            if name == "pow":
                return self._eval_binary(
                    BinaryOpNode(op="^", left=NumberNode(arg0), right=NumberNode(arg1))
                )
            if name == "atan2":
                rad = math.atan2(arg0, arg1)
                return self._from_radians(rad)

        # Single argument functions
        if len(node.args) != 1:
            raise CalculatorSyntaxError(
                f"Function '{node.name}' requires exactly one argument"
            )

        arg = self.evaluate(node.args[0])

        if name == "sin":
            return self._sin(arg)
        if name == "cos":
            return self._cos(arg)
        if name == "tan":
            return self._tan(arg)
        if name == "asin":
            return self._asin(arg)
        if name == "acos":
            return self._acos(arg)
        if name == "atan":
            return self._atan(arg)
        if name == "sinh":
            return math.sinh(arg)
        if name == "cosh":
            return math.cosh(arg)
        if name == "tanh":
            return math.tanh(arg)

        # Logarithm semantics per engineering rules:
        # log(x): base 10
        # log10(x): base 10
        # ln(x): natural logarithm
        if name in ("log", "log10"):
            if arg <= 0:
                raise CalculatorDomainError(
                    "Logarithm domain error: argument must be strictly positive"
                )
            return math.log10(arg)

        if name == "ln":
            if arg <= 0:
                raise CalculatorDomainError(
                    "Natural logarithm domain error: argument must be strictly positive"
                )
            return math.log(arg)

        if name == "sqrt":
            if arg < 0:
                raise CalculatorDomainError(
                    "Square root domain error: cannot take square root of negative number"
                )
            return math.sqrt(arg)

        if name == "cbrt":
            return (
                math.cbrt(arg)
                if hasattr(math, "cbrt")
                else (arg ** (1.0 / 3.0) if arg >= 0 else -((-arg) ** (1.0 / 3.0)))
            )

        if name == "exp":
            try:
                return math.exp(arg)
            except OverflowError as err:
                raise CalculatorOverflowError("Exponential function overflow") from err

        if name in ("abs", "fabs"):
            return math.fabs(arg)

        if name == "ceil":
            return float(math.ceil(arg))

        if name == "floor":
            return float(math.floor(arg))

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

    # =========================================================================
    # Trigonometry & Angle Conversions
    # =========================================================================

    def _to_radians(self, x: float) -> float:
        if self.angle_mode == AngleMode.DEG:
            return math.radians(x)
        if self.angle_mode == AngleMode.GRAD:
            return x * math.pi / 200.0
        return x

    def _from_radians(self, rad: float) -> float:
        if self.angle_mode == AngleMode.DEG:
            return math.degrees(rad)
        if self.angle_mode == AngleMode.GRAD:
            return rad * 200.0 / math.pi
        return rad

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
            if math.isclose(norm, 30.0, abs_tol=1e-12) or math.isclose(
                norm, 150.0, abs_tol=1e-12
            ):
                return 0.5
            if math.isclose(norm, 210.0, abs_tol=1e-12) or math.isclose(
                norm, 330.0, abs_tol=1e-12
            ):
                return -0.5
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
            if math.isclose(norm, 60.0, abs_tol=1e-12) or math.isclose(
                norm, 300.0, abs_tol=1e-12
            ):
                return 0.5
            if math.isclose(norm, 120.0, abs_tol=1e-12) or math.isclose(
                norm, 240.0, abs_tol=1e-12
            ):
                return -0.5
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
        half_pi = math.pi / 2.0
        norm_rad = (x - half_pi) % math.pi
        if math.isclose(norm_rad, 0.0, abs_tol=1e-12):
            raise CalculatorDomainError("tan is undefined at π/2 + kπ")
        return math.tan(x)

    def _asin(self, x: float) -> float:
        if x < -1.0 or x > 1.0:
            raise CalculatorDomainError("asin argument must be between -1 and 1")
        rad = math.asin(x)
        return self._from_radians(rad)

    def _acos(self, x: float) -> float:
        if x < -1.0 or x > 1.0:
            raise CalculatorDomainError("acos argument must be between -1 and 1")
        rad = math.acos(x)
        return self._from_radians(rad)

    def _atan(self, x: float) -> float:
        rad = math.atan(x)
        return self._from_radians(rad)
