#!/usr/bin/env python3
"""
Cross-platform packaging helper for Kira Calculator.

Usage:
    python scripts/build_app.py            # build for current platform
    python scripts/build_app.py --onefile  # single executable
"""

from __future__ import annotations

import argparse
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SPEC_DIR = ROOT / "packaging"


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.check_call(cmd, cwd=ROOT)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Kira Calculator package")
    parser.add_argument("--onefile", action="store_true", help="Produce a single executable")
    parser.add_argument("--name", default="KiraCalculator", help="Output name")
    args = parser.parse_args()

    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller is required. Install with:")
        print("  pip install pyinstaller")
        return 1

    entry = "src/kira_calculator/__main__.py"
    icon = ROOT / "assets" / "icons" / "kira-calculator.png"

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--windowed",          # no console on Windows/macOS
        "--name", args.name,
        "--paths", "src",
    ]

    if args.onefile:
        cmd.append("--onefile")
    else:
        cmd.append("--onedir")

    if icon.exists():
        cmd.extend(["--icon", str(icon)])

    # Collect Qt plugins / data
    cmd.extend([
        "--collect-all", "PySide6",
        "--collect-all", "shiboken6",
        entry,
    ])

    run(cmd)
    print(f"\nBuild finished. See: {DIST}")
    print(f"Platform: {platform.system()} {platform.machine()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
