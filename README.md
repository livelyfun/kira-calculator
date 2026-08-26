# Kira Calculator

A modern Linux desktop calculator written in Python and PySide6.

## Features

- **Standard & Scientific Calculation**: Arithmetic, powers, roots, percentages, logarithms, and trigonometric functions with DEG / RAD angle modes.
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
│   └── parser.py     # Expression parser & evaluator
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
