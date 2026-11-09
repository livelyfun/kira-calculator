# Kira Calculator

<p align="center">
  <img src="assets/icons/kira-calculator.png" alt="Kira Calculator logo" width="112">
</p>

<p align="center">
  <strong>A secure, cross-platform desktop calculator for everyday, scientific, programmer, and unit-conversion work.</strong>
</p>

<p align="center">
  <a href="https://github.com/livelyfun/kira-calculator/actions/workflows/ci.yml">
    <img src="https://github.com/livelyfun/kira-calculator/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI status">
  </a>
  <a href="https://github.com/livelyfun/kira-calculator/releases/latest">
    <img src="https://img.shields.io/github/v/release/livelyfun/kira-calculator" alt="Latest release">
  </a>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey" alt="Linux, Windows, and macOS">
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-AGPL--3.0--only-blue" alt="AGPL-3.0-only">
  </a>
</p>

<p align="center">
  <a href="#download">Download</a> ·
  <a href="#features">Features</a> ·
  <a href="#screenshots">Screenshots</a> ·
  <a href="#installation">Installation</a> ·
  <a href="#security">Security</a> ·
  <a href="#development">Development</a> ·
  <a href="#license">License</a>
</p>

---

## Why Kira Calculator?

Kira Calculator is a native desktop application built with Python and Qt 6 (PySide6). It combines four calculators in one focused interface:

- **Four modes in one app:** standard arithmetic, scientific functions, programmer operations, and unit conversion.
- **Safe by design:** expressions are tokenized, parsed, and evaluated by a constrained engine — never through Python `eval()` or `exec()`.
- **Native releases:** packaged standalone binaries for Linux, Windows, and macOS. Users do not need Python installed.
- **Local-first state:** preferences and calculation history are stored on your machine.
- **Comfortable to use:** dark and light themes, keyboard support, and responsive layouts.

## Download

**Get the latest standalone build from [GitHub Releases](https://github.com/livelyfun/kira-calculator/releases/latest).** Choose the asset matching your operating system. Standalone packages bundle the application and its Python/Qt runtime; a separate Python installation is not required.

| Platform | Download | How to run |
| --- | --- | --- |
| Linux x86_64 | `kira-calculator-<version>-linux-x86_64.tar.gz` | Extract, then run `./bin/kira-calculator` from the extracted folder |
| Windows x64 | `kira-calculator-windows-x64.zip` | Extract the ZIP, open the `kira-calculator` folder, then run `kira-calculator.exe` |
| macOS | `kira-calculator-macos.zip` | Extract, then move `kira-calculator.app` into Applications |

Release assets and exact filenames are shown on the [Releases page](https://github.com/livelyfun/kira-calculator/releases). Builds are produced on native GitHub-hosted Linux, Windows, and macOS runners. Check the release notes for the platforms included in each version.

## Features

- **Standard calculator:** everyday arithmetic, percentages, sign changes, and parentheses.
- **Scientific calculator:** trigonometric and hyperbolic functions, logarithms, powers, roots, factorials, constants, and DEG/RAD/GRAD angle modes.
- **Programmer calculator:** binary, octal, decimal, and hexadecimal; configurable 8/16/32/64-bit word sizes; signed and unsigned values; bitwise operations.
- **Unit converter:** length, mass, temperature, data, area, speed, time, and volume.
- **Persistent preferences and history:** theme, window state, angle mode, and calculation history are saved locally.
- **Dark and light themes:** switch between themes from the application.
- **Keyboard-first workflow:** calculate quickly with direct key bindings and mode shortcuts.

## Screenshots

<p align="center">
  <img src="docs/screenshots/standard_dark.png" alt="Standard calculator in dark theme" width="48%">
  <img src="docs/screenshots/scientific_dark.png" alt="Scientific calculator in dark theme" width="48%">
</p>
<p align="center">
  <img src="docs/screenshots/programmer.png" alt="Programmer calculator" width="48%">
  <img src="docs/screenshots/converter.png" alt="Unit converter" width="48%">
</p>

## Installation

### Linux installation

1. Download the Linux `.tar.gz` asset from the latest release.
2. Extract it:
   ```bash
   tar -xzf kira-calculator-*-linux-*.tar.gz
   cd kira-calculator
   ```
3. Launch:
   ```bash
   ./bin/kira-calculator
   ```

The archive also includes the project README, license, desktop entry, and icon.

### Windows installation

1. Download the Windows ZIP asset.
2. Extract it using File Explorer.
3. Open the `kira-calculator` folder and double-click `kira-calculator.exe`.

The archive includes the executable, README, license, and icon. If Windows SmartScreen displays an unknown-publisher warning, review the source and release provenance before choosing whether to run it. The project currently does not claim a signed Windows executable.

### macOS installation

1. Download and extract the macOS ZIP asset.
2. Move `kira-calculator.app` into Applications.
3. Open it from Finder. If macOS blocks it because the app is not signed or notarized, review the source and release provenance before deciding whether to allow it.

The macOS build is not currently code-signed or notarized.

### Verify a download

Every release publishes a `SHA256SUMS.txt` manifest alongside the platform archives. Download the release assets into one directory, then verify them on Linux or macOS:

```bash
sha256sum -c SHA256SUMS.txt
# macOS may use: shasum -a 256 -c SHA256SUMS.txt
```

On Windows PowerShell, compare the output of:

```powershell
Get-FileHash .\kira-calculator-windows-x64.zip -Algorithm SHA256
```

with the matching entry in `SHA256SUMS.txt`.

### Build from source

Requires Python 3.10 or newer:

```bash
git clone https://github.com/livelyfun/kira-calculator.git
cd kira-calculator
python -m venv .venv

# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -e .
kira-calculator
```

## Security

Expressions are treated as untrusted input and processed by a custom tokenizer, parser, and constrained AST evaluator. The calculation engine does not use Python `eval()`, `exec()`, or `asteval`. Input length, AST depth, node count, and exponent magnitude are bounded.

See [docs/security_model.md](docs/security_model.md) for the implementation's security assumptions and limits.

## Keyboard shortcuts

| Shortcut | Action |
| --- | --- |
| `0`–`9`, `.` | Enter numbers |
| `+`, `-`, `*`, `/` | Arithmetic |
| `^` | Exponentiation |
| `!` | Factorial |
| `%` | Percentage |
| `Enter` | Calculate |
| `Backspace` | Delete last character |
| `Escape` | Clear |
| `Ctrl+H` | Toggle history |
| `Ctrl+1`–`Ctrl+4` | Switch calculator modes |

## Development

Install development dependencies and run the checks:

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
ruff format --check .
```

The CI workflow runs linting, the test matrix across Python 3.10–3.13 on Linux, Windows, and macOS, and native packaging.

Build a standalone package on the current operating system:

```bash
python -m pip install -e ".[packaging]"

# Linux and Windows
python scripts/build_app.py --onefile

# macOS .app bundle
python scripts/build_app.py --onedir
```

Cross-platform release packages are built by [GitHub Actions](.github/workflows/ci.yml) on native Linux, Windows, and macOS runners. Push a version tag such as `v1.0.1` to trigger a GitHub Release after the lint, test, and packaging jobs succeed.

### Documentation

- [Architecture and design](docs/architecture.md)
- [Expression syntax reference](docs/expression_syntax.md)
- [Security model](docs/security_model.md)
- [Packaging and releases](docs/packaging.md)

## License

Kira Calculator is distributed under the **GNU Affero General Public License v3.0 only (AGPL-3.0-only)**. See [LICENSE](LICENSE).

Third-party dependencies retain their respective licenses.
