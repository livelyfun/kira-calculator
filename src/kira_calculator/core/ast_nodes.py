"""Abstract Syntax Tree (AST) node definitions for Kira Calculator expressions."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ASTNode:
    """Base class for all AST nodes."""


@dataclass(frozen=True)
class NumberNode(ASTNode):
    """Represents a numeric literal (integer or float)."""

    value: float


@dataclass(frozen=True)
class ConstantNode(ASTNode):
    """Represents a mathematical constant (e.g., pi, e, phi, tau)."""

    name: str


@dataclass(frozen=True)
class UnaryOpNode(ASTNode):
    """Represents a prefix unary operator such as + or -."""

    op: str
    operand: ASTNode


@dataclass(frozen=True)
class BinaryOpNode(ASTNode):
    """Represents a binary operator such as +, -, *, /, %, ^."""

    op: str
    left: ASTNode
    right: ASTNode


@dataclass(frozen=True)
class PostfixOpNode(ASTNode):
    """Represents a postfix operator such as factorial (!) or percentage (%)."""

    op: str
    operand: ASTNode


@dataclass(frozen=True)
class FunctionCallNode(ASTNode):
    """Represents a validated function call with explicit arguments."""

    name: str
    args: list[ASTNode] = field(default_factory=list)
