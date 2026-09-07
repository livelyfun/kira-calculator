# Kira Calculator – Architecture

## Overview

Kira Calculator is a cross-platform desktop scientific calculator built with **Python 3.10+** and **PySide6** (Qt 6).

Design goals:

- Safe evaluation (no bare `eval`)
- Clean separation of core logic and UI
- Easy packaging for Windows, macOS and Linux
- Extensible modes (Calculator, Programmer, Converter)
- Modern dark UI that matches the existing visual language

## High-level structure

```
src/kira_calculator/
├── __init__.py          # package metadata
├── __main__.py          # python -m kira_calculator
├── app.py               # QApplication bootstrap, high-DPI, stylesheet
├── core/
│   ├── engine.py        # asteval-based safe evaluator
│   ├── parser.py        # symbol normalisation (× → *, √ → sqrt, …)
│   └── history.py       # session + optional JSON persistence
└── ui/
    ├── main_window.py   # QMainWindow, layout, event routing
    ├── pages/
    │   ├── calculator_page.py
    │   ├── programmer_page.py   (scaffold)
    │   └── converter_page.py    (scaffold)
    ├── widgets/
    │   └── mode_bar.py          # exclusive mode switcher
    └── themes/
        └── dark.qss
```

## Core engine

- `prepare_expression()` normalises UI symbols.
- `evaluate()` / `calculate()` use a restricted `asteval.Interpreter`.
- Only a curated set of `math` functions and constants are exposed.
- Dangerous builtins (`open`, `exec`, `import`, …) are stripped.

## UI layer

- `CalculatorWindow` owns the display, mode stack and history panel.
- Each mode is a self-contained `QWidget` placed in a `QStackedWidget`.
- Mode bar uses `QButtonGroup` for exclusive selection.
- Keyboard support mirrors the on-screen buttons.
- History is persisted under `~/.kira_calculator/history.json`.

## Packaging

- Modern `pyproject.toml` with setuptools.
- Entry point: `kira-calculator` console script.
- Build helper: `scripts/build_app.py` (PyInstaller).
- Supports `--onefile` and `--onedir` modes.

## Future extensions

1. Full Programmer mode (bases + bitwise ops).
2. Unit Converter with live conversion.
3. Light / dark theme toggle.
4. Settings dialog (precision, angle unit, …).
5. Optional graphing panel.
