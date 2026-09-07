# Kira Calculator

A modern Linux desktop calculator written in Python and PySide6.

## Features

- **Standard Calculator**: Normal arithmetic with addition, subtraction, multiplication, division, decimals, parentheses, clear, backspace, and equals.
- **Scientific Calculator**: The standard keypad plus powers, roots, percentages, factorials, logarithms, trigonometric, inverse-trigonometric, and hyperbolic functions; constants; and DEG / RAD / GRAD angle modes.
- **Programmer Calculator**: The existing integer calculator page with BIN / OCT / DEC / HEX representations, a bit display, selectable word size, and signedness controls. Its behavior is intentionally preserved while a dedicated Programmer Mode refinement is planned.
- **Unit Converter**: An explicit application mode and page boundary. Unit conversions are not implemented yet.
- **Modern Linux GUI**: Clean, dark-themed Qt interface tailored for Linux desktop environments (such as KDE Plasma).
- **Calculation History**: Standard and Scientific modes share expression history, while Programmer and Converter retain their own page models.
- **Explicit Mode Architecture**: Standard, Scientific, Programmer, and Converter navigation is driven by a central `AppMode` model rather than stack indexes.

## Architecture

```text
User Expression
      ↓
Tokenizer
      ↓
Parser
      ↓
AST (Abstract Syntax Tree)
      ↓
Evaluator
      ↓
Result / CalculatorError
```

### Application modes

`AppMode` provides stable identifiers for all top-level modes. The window maps
those identifiers to pages with `QStackedWidget.setCurrentWidget`, so page order
is not part of the application contract. This leaves a clean path for future
keyboard shortcuts and saved mode preferences.

Standard and Scientific modes deliberately share the existing expression
display and history because both use the scientific expression engine.
Programmer has its own integer input and base/bit representation, and Converter
has its own page boundary for its future input/output controls.

## Getting Started

### Prerequisites

- Linux (Arch Linux, Ubuntu, Fedora, etc.)
- Python 3.10+
- PySide6

### Installation

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/livelyfun/kira-calculator.git
cd kira-calculator

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`.venv` is the project's supported local environment. Run commands through
`.venv/bin/python` when it is not activated.

### Running the Application

Launch the calculator:

```bash
python src/main.py
```

### Running Tests

Run the test suite with the project environment:

```bash
./.venv/bin/python -m pytest
```

### Code Formatting & Linting

We use [Ruff](https://github.com/astral-sh/ruff) for linting and code formatting:

```bash
# Lint check
ruff check .

# Auto-fix lint issues
ruff check --fix .

# Code formatting check
ruff format --check .

# Format code
ruff format .
```

## Project Structure

```text
src/
├── calculator/       # Mathematical expression engine
│   ├── logic.py      # Main calculation entry point
│   ├── tokenizer.py  # Lexer / Tokenizer
│   ├── parser.py     # Scientific expression parser
│   ├── programmer.py  # Programmer-mode integer engine
│   ├── evaluator.py   # Scientific AST evaluator
│   ├── ast_nodes.py   # Scientific AST node types
│   └── errors.py      # Shared calculation errors
├── styles/
│   └── main.qss      # Application stylesheet
├── ui/
│   ├── modes.py      # Central application-mode model
│   └── window.py     # Main application window
├── widgets/          # Reusable Qt widgets
│   ├── calculator_page.py
│   ├── scientific_page.py
│   ├── mode_bar.py
│   ├── programmer_page.py
│   └── converter_page.py
└── main.py           # Application entry point

tests/                # Test suite
```

## License

MIT License. See [LICENSE](LICENSE) for details.
