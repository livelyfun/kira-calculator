"""Security test suite verifying untrusted input rejection and resource bounding."""

import unittest

from kira_calculator.core.engine import evaluate_expression
from kira_calculator.core.errors import (
    CalculatorError,
    CalculatorOverflowError,
    CalculatorSyntaxError,
    SecurityError,
    UnknownFunctionError,
)


class TestExpressionSecurity(unittest.TestCase):
    def test_reject_imports(self):
        injections = [
            "__import__('os').system('echo pwned')",
            "import os",
            "import sys",
            "from math import *",
        ]
        for expr in injections:
            res = evaluate_expression(expr)
            self.assertFalse(res.success, f"Failed to reject import: {expr}")
            self.assertIsInstance(res.error, CalculatorError)

    def test_reject_attribute_access(self):
        injections = [
            "(1).__class__",
            "(1).toString()",
            "'abc'.upper()",
            "math.__dict__",
            "pi.__class__.__base__.__subclasses__()",
        ]
        for expr in injections:
            res = evaluate_expression(expr)
            self.assertFalse(res.success, f"Failed to reject attribute access: {expr}")
            self.assertIsInstance(res.error, CalculatorError)

    def test_reject_arbitrary_function_calls(self):
        calls = [
            "eval('2+2')",
            "exec('x=1')",
            "open('/etc/passwd')",
            "system('ls')",
            "exit()",
            "quit()",
            "getattr(math, 'sin')",
            "setattr(x, 'y', 1)",
            "globals()",
            "locals()",
        ]
        for expr in calls:
            res = evaluate_expression(expr)
            self.assertFalse(res.success, f"Failed to reject arbitrary function call: {expr}")
            self.assertIsInstance(res.error, (UnknownFunctionError, CalculatorSyntaxError))

    def test_reject_assignment_and_code_blocks(self):
        blocks = [
            "x = 5",
            "x := 10",
            "def foo(): pass",
            "lambda x: x * 2",
            "class A: pass",
        ]
        for expr in blocks:
            res = evaluate_expression(expr)
            self.assertFalse(res.success, f"Failed to reject code statement: {expr}")
            self.assertIsInstance(res.error, CalculatorError)

    def test_bound_nesting_depth(self):
        # 150 nested parentheses exceeds MAX_DEPTH = 100
        deep_expr = "(" * 150 + "1" + ")" * 150
        res = evaluate_expression(deep_expr)
        self.assertFalse(res.success)
        self.assertIsInstance(res.error, SecurityError)

    def test_bound_excessive_expression_length(self):
        # 3000 chars exceeds MAX_EXPRESSION_LENGTH = 2000
        huge_expr = "1 + " * 800 + "1"
        res = evaluate_expression(huge_expr)
        self.assertFalse(res.success)
        self.assertIsInstance(res.error, SecurityError)

    def test_bound_excessive_exponents(self):
        res = evaluate_expression("10 ^ 50000")
        self.assertFalse(res.success)
        self.assertIsInstance(res.error, CalculatorOverflowError)

    def test_bound_excessive_factorials(self):
        res = evaluate_expression("5000!")
        self.assertFalse(res.success)
        self.assertIsInstance(res.error, CalculatorOverflowError)


if __name__ == "__main__":
    unittest.main()

