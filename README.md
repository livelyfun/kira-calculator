# Kira Calculator

<p align="center">
  <img src="assets/icons/kira-calculator.png" alt="Kira Calculator Logo" width="128" height="128">
</p>

<p align="center">
  <b>A modern, mathematically rigorous, secure, cross-platform desktop calculator.</b>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#supported-modes">Modes</a> •
  <a href="#installation--packaging">Installation</a> •
  <a href="#keyboard-shortcuts">Shortcuts</a> •
  <a href="#security-model">Security</a> •
  <a href="#development">Development</a> •
  <a href="#license">License</a>
</p>

---

## Overview

**Kira Calculator** is an enterprise-grade desktop calculator application engineered with **Python 3.10+** and **PySide6 (Qt6)**. Designed to surpass typical default calculator utilities, Kira combines a custom recursive-descent mathematical engine with a refined, customizable user interface.

Unlike naive calculators that rely on Python's insecure `eval()` or unconstrained interpreters, Kira processes all user expressions through an isolated lexical analyzer, grammar parser, and type-checked Abstract Syntax Tree (AST) evaluator with deterministic resource limits.

---

## Visual Showcase

<p align="center">
  <img src="docs/screenshots/standard_dark.png" alt="Standard Mode Dark" width="48%">
  <img src="docs/screenshots/scientific_dark.png" alt="Scientific Mode Dark" width="48%">
</p>
<p align="center">
  <img src="docs/screenshots/programmer.png" alt="Programmer Mode" width="48%">
  <img src="docs/screenshots/converter.png" alt="Unit Converter Mode" width="48%">
</p>

---

## Features

- **Mathematically Trustworthy:** Strict operator precedence, right-associative powers (`2^3^2 = 512`), exact unary negation (`-2^2 = -4`), and noise-free floating-point formatting (`0.1 + 0.2 = 0.3`).
- **Four Dedicated Calculation Modes:** Standard, Scientific, Programmer, and Unit Converter.
- **Robust Security Architecture:** Zero arbitrary code execution. Evaluator rejects imports, code blocks, attribute traversals, and excessive resource consumption.
- **Persistent State:** Calculation history and user preferences (theme, geometry, angle mode) persist across restarts using atomic JSON writes.
- **Multi-Theme Engine:** High-contrast Dark theme and crisp Light theme with instant switching.
- **Keyboard-First Experience:** Full numeric keypad, standard arithmetic operators, and dedicated hotkeys for every action.
- **Standalone Distribution:** PyInstaller packaging bundles all Qt plugins and assets with no Python runtime required.

---

## Supported Modes

### 1. Standard Mode
Simple everyday arithmetic with an intuitive keypad layout, percentage calculations, sign toggling, and instant calculation display.

### 2. Scientific Mode
- **Trigonometric:** `sin`, `cos`, `tan`, `asin`, `acos`, `atan`
- **Hyperbolic:** `sinh`, `cosh`, `tanh`
- **Logarithmic:** `log` (base 10), `log10` (base 10), `ln` (natural logarithm)
- **Powers & Roots:** `xʸ`, `x²`, `sqrt` (`√`), `cbrt`
- **Combinatorics:** Factorials (`n!`), bounded to $n \le 170$
- **Mathematical Constants:** $\pi$ (`pi`), $e$, $\phi$ (Golden Ratio), $\tau$ (`tau`)
- **Angle Modes:** Live toggling between `DEG` (Degrees), `RAD` (Radians), and `GRAD` (Gradians).

### 3. Programmer Mode
- **Bases:** Real-time multi-base synchronization across **Binary (BIN)**, **Octal (OCT)**, **Decimal (DEC)**, and **Hexadecimal (HEX)**.
- **Word Sizes:** 8-bit, 16-bit, 32-bit, and 64-bit integer masks.
- **Signedness:** Signed (two's complement) and Unsigned modes.
- **Bitwise Logic:** `AND`, `OR`, `XOR`, `NOT`, and bit shifts (`<<`, `>>`).
- **Interactive Visualizer:** Visual 32/64-bit binary grid with grouped nibbles.

### 4. Unit Converter Mode
Bidirectional, real-time conversion across 8 physical and digital domains:
- **Length:** Meter, Kilometer, Centimeter, Millimeter, Mile, Yard, Foot, Inch, Nautical Mile.
- **Mass:** Kilogram, Gram, Milligram, Metric Ton, Pound, Ounce, Stone.
- **Temperature:** Celsius (°C), Fahrenheit (°F), Kelvin (K).
- **Data:** Byte, Kilobyte, Megabyte, Gigabyte, Terabyte, Petabyte, Kibibyte, Mebibyte, Gibibyte, Tebibyte.
- **Area:** Square Meter, Square Kilometer, Square Foot, Square Mile, Acre, Hectare.
- **Speed:** Meter/sec, Kilometer/hour, Mile/hour, Knot, Foot/sec.
- **Time:** Millisecond, Second, Minute, Hour, Day, Week, Year.
- **Volume:** Liter, Milliliter, Cubic Meter, Gallon, Quart, Pint, Cup, Fluid Ounce.

---

## Installation & Packaging

### Standalone Linux AppImage
The simplest way to run Kira Calculator on any modern Linux distribution without installing Python:
```bash
# Make AppImage executable and launch
chmod +x dist/kira-calculator-1.0.0-x86_64.AppImage
./dist/kira-calculator-1.0.0-x86_64.AppImage
```

### Standalone Executable & Release Tarball (Linux)
```bash
# Extract the release tarball
tar -xzf dist/kira-calculator-1.0.0-linux-x86_64.tar.gz
cd kira-calculator

# Launch the standalone binary
./bin/kira-calculator
```

### Checksum Verification
```bash
cd dist
sha256sum -c kira-calculator-1.0.0-x86_64.AppImage.sha256
sha256sum -c kira-calculator-1.0.0-linux-x86_64.tar.gz.sha256
```

### Run from Source
```bash
# Clone the repository
git clone https://github.com/livelyfun/kira-calculator.git
cd kira-calculator

# Install dependencies in editable mode
pip install -e .

# Launch application
kira-calculator
# or
python3 -m kira_calculator
```

---

## Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| `0` - `9`, `.` | Numeric input |
| `+`, `-`, `*`, `/` | Addition, Subtraction, Multiplication (`×`), Division (`÷`) |
| `^` | Exponentiation / Power |
| `!` | Factorial |
| `%` | Percentage |
| `(` , `)` | Parentheses |
| `Enter` / `Return` | Calculate result |
| `Backspace` | Delete last character |
| `Escape` | Clear display (`C`) |
| `Ctrl + H` | Toggle calculation history drawer |
| `Ctrl + 1` | Switch to Standard Mode |
| `Ctrl + 2` | Switch to Scientific Mode |
| `Ctrl + 3` | Switch to Programmer Mode |
| `Ctrl + 4` | Switch to Converter Mode |

---

## Security Model

Kira Calculator treats all input expressions as untrusted strings:
- **Zero Insecure Interpreters:** No `eval()`, `exec()`, or `asteval`.
- **Whitelisted AST Grammar:** Only mathematical tokens parsed into immutable node classes.
- **Bounded Resource Consumption:** Expressions capped at 2,000 characters; AST depth capped at 100 levels; AST nodes capped at 1,000; exponents capped at $|exp| \le 10,000$.

Refer to [`docs/security_model.md`](docs/security_model.md) for detailed threat modeling.

---

## Development & Testing

### Running Tests
```bash
# Run full automated test suite (72 tests)
pytest -v

# Run with coverage
pytest --cov=src/kira_calculator tests/
```

### Code Style & Linting
```bash
# Check code style with Ruff
ruff check .

# Format code
ruff format .
```

### Packaging Builds
```bash
# Build standalone single-file binary and release tarball
python3 scripts/build_app.py --onefile
```

---

## License

This project is licensed under the [MIT License](LICENSE).
