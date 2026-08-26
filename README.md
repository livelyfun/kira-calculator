# Kira Calculator

A modern Linux desktop calculator written in Python and PySide6.

## Features

- **Standard & Scientific Calculation**: Arithmetic, powers, roots, percentages, logarithms, and trigonometric functions with DEG / RAD / GRAD angle modes.
- **Programmer Calculation**: Base conversion (BIN / OCT / DEC / HEX), integer arithmetic, bitwise operations, shifts, selectable word sizes, and two's-complement signed mode.
- **Modern Linux GUI**: Clean, dark-themed Qt interface tailored for Linux desktop environments (such as KDE Plasma).
- **Calculation History**: Track, restore, and clear previous expressions and results.
- **Extensible Architecture**: Modular separation between expression engine, services, and UI components.

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

### Programmer mode semantics

Programmer mode stores values as bit patterns and masks every operation to the
selected 8-, 16-, 32-, or 64-bit word size. Unsigned mode displays values from
zero through the word-size maximum. Signed mode interprets the same pattern as
two's-complement, displays negative values with a leading `-`, and uses an
arithmetic right shift. Input values are range-checked; arithmetic overflow
wraps modulo the selected word size. Division truncates toward zero, and
negative values require signed mode.

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
│   └── window.py     # Main application window
├── widgets/          # Reusable Qt widgets
│   ├── calculator_page.py
│   ├── mode_bar.py
│   ├── programmer_page.py
│   └── converter_page.py
└── main.py           # Application entry point

tests/                # Test suite
```

## License

MIT License. See [LICENSE](LICENSE) for details.
