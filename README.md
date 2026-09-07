# Kira Calculator 🧮

A modern, **safe**, cross-platform scientific calculator built with **Python** and **PySide6**.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![PySide6](https://img.shields.io/badge/PySide6-6.6%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- Scientific calculator (sin, cos, tan, log, ln, √, π, e, powers, …)
- Safe expression engine – **never uses bare `eval()`**
- Clean dark UI with history panel
- Keyboard support
- Mode switcher (Calculator / Programmer / Converter – last two are scaffolds)
- Persistent history (`~/.kira_calculator/history.json`)
- Works on **Windows, macOS and Linux**
- Proper packaging (installable package + PyInstaller builds)

## 🚀 Quick Start

### From source (recommended for development)

```bash
git clone https://github.com/livelyfun/kira-calculator.git
cd kira-calculator

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -e .
kira-calculator
# or
python -m kira_calculator
```

### Dependencies only

```bash
pip install -r requirements.txt
PYTHONPATH=src python -m kira_calculator
```

## 🧪 Tests

```bash
pip install -e ".[dev]"
pytest
```

## 📦 Packaging into a standalone app

```bash
pip install -e ".[packaging]"
python scripts/build_app.py            # folder build
python scripts/build_app.py --onefile  # single executable
```

See [docs/packaging.md](docs/packaging.md) for platform-specific notes.

## 🏗️ Project Structure

```
kira-calculator/
├── src/kira_calculator/     # main package
│   ├── core/                # safe engine, parser, history
│   ├── ui/                  # windows, pages, themes
│   └── app.py
├── tests/
├── docs/
├── scripts/build_app.py
├── assets/icons/
├── pyproject.toml
└── requirements.txt
```

## 📖 Documentation

- [Architecture](docs/architecture.md)
- [Packaging](docs/packaging.md)

## 🛡️ Safety

The expression engine uses **asteval** with a restricted symbol table. Dangerous operations (`open`, `exec`, `import`, …) are unavailable.

## 👤 Author

[Mithlesh Das](https://github.com/livelyfun) — BIT undergraduate and aspiring backend & full-stack developer based in Biratnagar, Nepal.

## 📄 License

MIT – see [LICENSE](LICENSE).
