"""Kira Calculator: Modern, safe, cross-platform desktop calculator."""

__version__ = "1.0.0"
__author__ = "Kira Calculator Contributors"

from .app import create_application, main
from .core.engine import calculate, evaluate_expression

__all__ = [
    "calculate",
    "create_application",
    "evaluate_expression",
    "main",
]

