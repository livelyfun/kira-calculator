# Kira Calculator: Packaging & Release Guide

## 1. Overview

Kira Calculator is distributed as a standalone desktop application across Linux, Windows, and macOS without requiring end users to pre-install Python or Qt.

Packaging is managed via PyInstaller with platform-specific asset bundling and metadata generation.

---

## 2. Linux Packaging

### Artifacts Delivered
- **Standalone Single Binary:** `dist/kira-calculator`
- **Distributable Release Tarball:** `dist/kira-calculator-1.0.0-linux-x86_64.tar.gz`
- **SHA256 Checksum:** `dist/kira-calculator-1.0.0-linux-x86_64.tar.gz.sha256`
- **Desktop Launcher File:** `packaging/linux/kira-calculator.desktop`
- **HiDPI Icon:** `assets/icons/kira-calculator.png`

### Building Standalone Linux Executable
```bash
# Build standalone single-file binary with embedded assets
python3 scripts/build_app.py --onefile

# Build folder-based distribution
python3 scripts/build_app.py
```

### Installation from Tarball
```bash
tar -xzf dist/kira-calculator-1.0.0-linux-x86_64.tar.gz
cd kira-calculator

# Run directly
./kira-calculator

# Or install to user desktop environment
cp share/applications/kira-calculator.desktop ~/.local/share/applications/
cp share/icons/hicolor/256x256/apps/kira-calculator.png ~/.local/share/icons/
```

---

## 3. Windows & macOS CI Packaging

Packaging for Windows and macOS is executed via the GitHub Actions CI matrix on native virtual environments:
- **Windows (`windows-latest`):** Builds standalone `kira-calculator.exe` with bundled Qt DLLs and application icon.
- **macOS (`macos-latest`):** Builds standalone `kira-calculator.app` bundle with high-DPI icon and Retina display support.

---

## 4. Verification Checklist for Packaged Binaries

Each build must verify:
- [x] Launches on a clean system without Python installed.
- [x] Loads Dark and Light themes correctly from bundled resources.
- [x] Standard mode arithmetic and precedence work.
- [x] Scientific mode with DEG, RAD, and GRAD angle calculations works.
- [x] Programmer mode multi-base conversion and bit grid work.
- [x] Converter mode bidirectional unit conversions work.
- [x] History entries persist across application restarts in platform data directory.
- [x] User settings persist across restarts in platform config directory.
- [x] Application closes cleanly with status code 0.

