"""Direct execution module for python -m kira_calculator."""

import sys

try:
    from kira_calculator.app import main
except ImportError:
    from .app import main

if __name__ == "__main__":
    sys.exit(main())
