# Packaging & Distribution

## Development install

```bash
git clone https://github.com/livelyfun/kira-calculator.git
cd kira-calculator
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
kira-calculator                    # or: python -m kira_calculator
```

## Running tests

```bash
pytest
```

## Building a standalone app

```bash
pip install ".[packaging]"
python scripts/build_app.py            # onedir build
python scripts/build_app.py --onefile  # single executable
```

Output appears in `dist/`.

### Platform notes

| Platform | Recommended | Notes |
|----------|-------------|-------|
| Windows  | `--onefile` or `--onedir` | Use a `.ico` for best results |
| macOS    | `--onedir` + `.app` bundle | Codesign for distribution |
| Linux    | AppImage or `--onedir` | AppImage can be built with additional tools |

## Icon

Place a high-resolution PNG at:

```
assets/icons/kira-calculator.png
```

The build script and the main window will pick it up automatically when present.
