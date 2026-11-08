"""Legacy root launcher delegating to kira_calculator.app."""

import sys
from pathlib import Path

# Add src directory to sys.path if not present
src_dir = Path(__file__).resolve().parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from kira_calculator.app import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
