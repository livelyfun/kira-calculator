#!/usr/bin/env python3
"""Cross-platform build, optimization, and packaging script for Kira Calculator."""

from __future__ import annotations

import argparse
import hashlib
import os
import platform
import shutil
import stat
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
BUILD = ROOT / "build"
PACKAGING = ROOT / "packaging"

EXCLUDED_MODULES = [
    "PySide6.QtWebEngineCore",
    "PySide6.QtWebEngineWidgets",
    "PySide6.QtWebEngineQuick",
    "PySide6.Qt3DAnimation",
    "PySide6.Qt3DCore",
    "PySide6.Qt3DExtras",
    "PySide6.Qt3DInput",
    "PySide6.Qt3DLogic",
    "PySide6.Qt3DRender",
    "PySide6.QtQuick",
    "PySide6.QtQuick3D",
    "PySide6.QtQuickControls2",
    "PySide6.QtQuickTest",
    "PySide6.QtQuickWidgets",
    "PySide6.QtQml",
    "PySide6.QtMultimedia",
    "PySide6.QtMultimediaWidgets",
    "PySide6.QtBluetooth",
    "PySide6.QtPositioning",
    "PySide6.QtSensors",
    "PySide6.QtSerialPort",
    "PySide6.QtSerialBus",
    "PySide6.QtWebSockets",
    "PySide6.QtWebView",
    "PySide6.QtPdf",
    "PySide6.QtPdfWidgets",
    "PySide6.QtSpatialAudio",
    "PySide6.QtNfc",
    "PySide6.QtRemoteObjects",
    "PySide6.QtScxml",
    "PySide6.QtTextToSpeech",
    "PySide6.QtCharts",
    "PySide6.QtDataVisualization",
    "PySide6.QtGraphs",
    "PySide6.QtHttpServer",
    "PySide6.QtLocation",
    "PySide6.QtNetworkAuth",
    "PySide6.QtVirtualKeyboard",
    "tkinter",
    "matplotlib",
    "numpy",
    "scipy",
    "asteval",
    "pytest",
    "ruff",
]


def sha256_file(path: Path) -> str:
    """Compute sha256 hexadecimal hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def run_command(cmd: list[str]) -> None:
    print(f"+ {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd=ROOT)


def build_pyinstaller(onefile: bool = False, clean: bool = True) -> Path:
    """Invoke PyInstaller to generate optimized standalone binaries."""
    entry = ROOT / "src" / "kira_calculator" / "__main__.py"
    icon = ROOT / "assets" / "icons" / "kira-calculator.png"

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--windowed",
        "--name",
        "kira-calculator",
        "--specpath",
        str(PACKAGING),
        "--paths",
        "src",
        "--hidden-import",
        "PySide6.QtCore",
        "--hidden-import",
        "PySide6.QtGui",
        "--hidden-import",
        "PySide6.QtWidgets",
        "--add-data",
        f"{ROOT / 'src' / 'kira_calculator' / 'ui' / 'themes'}:kira_calculator/ui/themes",
        "--add-data",
        f"{ROOT / 'assets' / 'icons'}:assets/icons",
    ]

    if clean:
        cmd.append("--clean")

    # Add exclusions to dramatically reduce binary size
    for mod in EXCLUDED_MODULES:
        cmd.extend(["--exclude-module", mod])

    if onefile:
        cmd.append("--onefile")
    else:
        cmd.append("--onedir")

    if icon.exists() and not sys.platform.startswith("linux"):
        cmd.extend(["--icon", str(icon)])

    cmd.append(str(entry))
    run_command(cmd)

    output_path = DIST / ("kira-calculator" if not sys.platform.startswith("win") else "kira-calculator.exe")
    if not onefile:
        output_path = DIST / "kira-calculator" / ("kira-calculator" if not sys.platform.startswith("win") else "kira-calculator.exe")

    return output_path


def package_tarball(app_dir: Path, version: str = "1.0.0") -> Path:
    """Create a distributable tarball for Linux with desktop file and icon."""
    system_tag = platform.system().lower()
    machine_tag = platform.machine().lower()
    archive_name = f"kira-calculator-{version}-{system_tag}-{machine_tag}.tar.gz"
    archive_path = DIST / archive_name

    print(f"\nCreating release archive: {archive_path}")
    with tarfile.open(archive_path, "w:gz") as tar:
        # Add the application folder or binary
        if app_dir.is_dir():
            tar.add(app_dir, arcname="kira-calculator")
        else:
            tar.add(app_dir, arcname="kira-calculator/bin/kira-calculator")

        # Add desktop entry and icon
        desktop_file = PACKAGING / "linux" / "kira-calculator.desktop"
        if desktop_file.exists():
            tar.add(desktop_file, arcname="kira-calculator/share/applications/kira-calculator.desktop")

        icon_file = ROOT / "assets" / "icons" / "kira-calculator.png"
        if icon_file.exists():
            tar.add(icon_file, arcname="kira-calculator/share/icons/hicolor/256x256/apps/kira-calculator.png")

        # Add README and LICENSE
        readme = ROOT / "README.md"
        if readme.exists():
            tar.add(readme, arcname="kira-calculator/README.md")
        license_file = ROOT / "LICENSE"
        if license_file.exists():
            tar.add(license_file, arcname="kira-calculator/LICENSE")

    checksum = sha256_file(archive_path)
    # Correct filename: exact .tar.gz.sha256 extension
    checksum_file = archive_path.parent / f"{archive_path.name}.sha256"
    checksum_file.write_text(f"{checksum}  {archive_name}\n")
    print(f"Archive SHA256: {checksum} -> {checksum_file.name}")
    return archive_path


def package_appimage(binary_path: Path, version: str = "1.0.0") -> Path | None:
    """Create a standalone AppImage for Linux."""
    appimagetool = PACKAGING / "tools" / "appimagetool"
    if not appimagetool.exists():
        print("Note: packaging/tools/appimagetool not found; skipping AppImage build.")
        return None

    print("\n=== Building Linux AppImage ===")
    app_dir = DIST / "AppDir"
    if app_dir.exists():
        shutil.rmtree(app_dir)

    usr_bin = app_dir / "usr" / "bin"
    usr_bin.mkdir(parents=True, exist_ok=True)
    usr_apps = app_dir / "usr" / "share" / "applications"
    usr_apps.mkdir(parents=True, exist_ok=True)
    usr_icons = app_dir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps"
    usr_icons.mkdir(parents=True, exist_ok=True)

    # Copy binary
    target_bin = usr_bin / "kira-calculator"
    shutil.copy2(binary_path, target_bin)
    target_bin.chmod(target_bin.stat().st_mode | stat.S_IEXEC)

    # Copy desktop file and icon
    desktop_src = PACKAGING / "linux" / "kira-calculator.desktop"
    shutil.copy2(desktop_src, app_dir / "kira-calculator.desktop")
    shutil.copy2(desktop_src, usr_apps / "kira-calculator.desktop")

    icon_src = ROOT / "assets" / "icons" / "kira-calculator.png"
    if icon_src.exists():
        shutil.copy2(icon_src, app_dir / "kira-calculator.png")
        shutil.copy2(icon_src, app_dir / ".DirIcon")
        shutil.copy2(icon_src, usr_icons / "kira-calculator.png")

    # Copy appstream metainfo if present
    appdata_src = PACKAGING / "linux" / "kira-calculator.appdata.xml"
    if appdata_src.exists():
        metainfo_dir = app_dir / "usr" / "share" / "metainfo"
        metainfo_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(appdata_src, metainfo_dir / "kira-calculator.appdata.xml")

    # Create AppRun launcher
    apprun = app_dir / "AppRun"
    apprun.write_text("""#!/bin/sh
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"
exec "${HERE}/usr/bin/kira-calculator" "$@"
""")

    # Ensure executable permissions for all users (0755)
    target_bin.chmod(0o755)
    apprun.chmod(0o755)
    subprocess.check_call(["chmod", "-R", "a+rX", str(app_dir)])

    appimage_name = f"kira-calculator-{version}-x86_64.AppImage"
    appimage_path = DIST / appimage_name

    cmd = [
        str(appimagetool),
        "--appimage-extract-and-run",
        "--no-appstream",
        "--runtime-file",
        str(PACKAGING / "tools" / "runtime-x86_64"),
        str(app_dir),
        str(appimage_path),
    ]
    env = os.environ.copy()
    env["ARCH"] = "x86_64"
    print(f"+ {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd=ROOT, env=env)

    # Compute checksum
    checksum = sha256_file(appimage_path)
    checksum_file = appimage_path.parent / f"{appimage_name}.sha256"
    checksum_file.write_text(f"{checksum}  {appimage_name}\n")
    print(f"AppImage SHA256: {checksum} -> {checksum_file.name}")

    # Cleanup temporary AppDir
    shutil.rmtree(app_dir, ignore_errors=True)
    return appimage_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and package Kira Calculator")
    parser.add_argument("--onefile", action="store_true", default=True, help="Build single standalone executable")
    parser.add_argument("--tarball", action="store_true", default=True, help="Create distributable archive")
    parser.add_argument("--appimage", action="store_true", default=True, help="Create AppImage (Linux)")
    parser.add_argument("--no-clean", action="store_true", help="Do not clean build cache before building")
    args = parser.parse_args()

    print(f"=== Building Optimized Kira Calculator on {platform.system()} ({platform.machine()}) ===")
    binary_path = build_pyinstaller(onefile=args.onefile, clean=not args.no_clean)

    if not binary_path.exists():
        print(f"ERROR: Build output {binary_path} was not created!", file=sys.stderr)
        return 1

    size_mb = binary_path.stat().st_size / (1024 * 1024)
    print(f"\nSuccessfully built optimized binary: {binary_path} ({size_mb:.1f} MB)")

    if args.tarball and platform.system().lower() == "linux":
        dist_dir = DIST / "kira-calculator" if not args.onefile else binary_path
        package_tarball(dist_dir)

    if args.appimage and platform.system().lower() == "linux":
        package_appimage(binary_path)

    print("\nPackaging completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
