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
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
BUILD = ROOT / "build"
PACKAGING = ROOT / "packaging"
APP_NAME = "kira-calculator"

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


def get_project_version() -> str:
    """Read authoritative version from pyproject.toml."""
    pyproject_path = ROOT / "pyproject.toml"
    if pyproject_path.exists():
        try:
            import tomllib

            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)
            ver = data.get("project", {}).get("version")
            if ver:
                return str(ver)
        except Exception:
            pass
        import re

        content = pyproject_path.read_text(encoding="utf-8")
        match = re.search(r'version\s*=\s*"([^"]+)"', content)
        if match:
            return match.group(1)

    try:
        from kira_calculator import __version__

        return __version__
    except Exception:
        return "1.0.0"


def validate_tag(tag: str) -> bool:
    """Validate that a git tag string matches the project version."""
    clean_tag = tag.strip()
    if clean_tag.startswith("refs/tags/"):
        clean_tag = clean_tag[len("refs/tags/") :]
    if clean_tag.startswith("v"):
        clean_tag = clean_tag[1:]
    project_version = get_project_version()
    return clean_tag == project_version


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


def build_pyinstaller(onefile: bool = True, clean: bool = True) -> Path:
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

    if sys.platform == "darwin":
        # PyInstaller creates a macOS .app bundle for windowed applications.
        output_path = DIST / "kira-calculator.app"
    else:
        output_path = DIST / (
            "kira-calculator.exe" if sys.platform.startswith("win") else "kira-calculator"
        )
        if not onefile:
            output_path = (
                DIST
                / "kira-calculator"
                / (
                    "kira-calculator.exe"
                    if sys.platform.startswith("win")
                    else "kira-calculator"
                )
            )

    return output_path


def archive_target(output_path: Path, onefile: bool) -> Path:
    """Return the file or directory that the platform archive should contain."""
    if sys.platform == "darwin":
        # A windowed macOS build is always distributed as an .app bundle,
        # regardless of whether its executable was built as onefile or onedir.
        return DIST / f"{APP_NAME}.app"
    if onefile:
        return output_path
    return DIST / APP_NAME


def package_tarball(app_dir: Path, version: str | None = None) -> Path:
    """Create a distributable tarball for Linux with desktop file and icon."""
    ver = version or get_project_version()
    machine_tag = platform.machine().lower()
    if machine_tag in ("amd64", "x86_64"):
        machine_tag = "x86_64"
    archive_name = f"kira-calculator-{ver}-linux-{machine_tag}.tar.gz"
    archive_path = DIST / archive_name

    print(f"\nCreating Linux release archive: {archive_path}")
    with tarfile.open(archive_path, "w:gz") as tar:
        # Add the application folder or binary
        if app_dir.is_dir():
            tar.add(app_dir, arcname="kira-calculator")
        else:
            tar.add(app_dir, arcname="kira-calculator/bin/kira-calculator")

        # Add desktop entry and icon
        desktop_file = PACKAGING / "linux" / "kira-calculator.desktop"
        if desktop_file.exists():
            tar.add(
                desktop_file,
                arcname="kira-calculator/share/applications/kira-calculator.desktop",
            )

        icon_file = ROOT / "assets" / "icons" / "kira-calculator.png"
        if icon_file.exists():
            tar.add(
                icon_file,
                arcname="kira-calculator/share/icons/hicolor/256x256/apps/kira-calculator.png",
            )

        # Add README and LICENSE
        readme = ROOT / "README.md"
        if readme.exists():
            tar.add(readme, arcname="kira-calculator/README.md")
        license_file = ROOT / "LICENSE"
        if license_file.exists():
            tar.add(license_file, arcname="kira-calculator/LICENSE")

    checksum = sha256_file(archive_path)
    checksum_file = archive_path.parent / f"{archive_path.name}.sha256"
    checksum_file.write_text(f"{checksum}  {archive_name}\n")
    print(f"Archive SHA256: {checksum} -> {checksum_file.name}")
    return archive_path


def package_zip_windows(binary_path: Path, version: str | None = None) -> Path:
    """Create a distributable ZIP archive for Windows."""
    archive_name = "kira-calculator-windows-x64.zip"
    archive_path = DIST / archive_name

    print(f"\nCreating Windows release archive: {archive_path}")
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
        if binary_path.is_dir():
            for root, _, files in os.walk(binary_path):
                for file in files:
                    full_path = Path(root) / file
                    rel = full_path.relative_to(binary_path)
                    zf.write(full_path, arcname=f"kira-calculator/{rel}")
        else:
            zf.write(binary_path, arcname=f"kira-calculator/{binary_path.name}")

        readme = ROOT / "README.md"
        if readme.exists():
            zf.write(readme, arcname="kira-calculator/README.md")
        license_file = ROOT / "LICENSE"
        if license_file.exists():
            zf.write(license_file, arcname="kira-calculator/LICENSE")
        icon_file = ROOT / "assets" / "icons" / "kira-calculator.png"
        if icon_file.exists():
            zf.write(icon_file, arcname="kira-calculator/kira-calculator.png")

    checksum = sha256_file(archive_path)
    checksum_file = archive_path.parent / f"{archive_path.name}.sha256"
    checksum_file.write_text(f"{checksum}  {archive_name}\n")
    print(f"Archive SHA256: {checksum} -> {checksum_file.name}")
    return archive_path


def package_zip_macos(target_path: Path, version: str | None = None) -> Path:
    """Create a distributable ZIP archive for macOS.

    On macOS, ``ditto`` is used so the ``.app`` bundle keeps its symlinks and
    extended attributes. Other platforms fall back to ``zipfile`` for local
    archive inspection and testing.
    """
    archive_name = "kira-calculator-macos.zip"
    archive_path = DIST / archive_name
    if archive_path.exists():
        archive_path.unlink()

    print(f"\nCreating macOS release archive: {archive_path}")

    if sys.platform == "darwin" and shutil.which("ditto"):
        staging = DIST / "macos-release"
        shutil.rmtree(staging, ignore_errors=True)
        staging.mkdir(parents=True)
        try:
            destination = staging / target_path.name
            if target_path.is_dir():
                shutil.copytree(target_path, destination, symlinks=True)
            else:
                shutil.copy2(target_path, destination)

            for doc_name in ("README.md", "LICENSE"):
                doc = ROOT / doc_name
                if doc.exists():
                    shutil.copy2(doc, staging / doc_name)

            # Archive the staging directory's contents (no --keepParent) so the
            # .app bundle, README, and LICENSE sit at the root of the ZIP.
            subprocess.check_call(
                [
                    "ditto",
                    "-c",
                    "-k",
                    "--sequesterRsrc",
                    str(staging),
                    str(archive_path),
                ]
            )
        finally:
            shutil.rmtree(staging, ignore_errors=True)
    else:
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
            if target_path.is_dir():
                for root, _, files in os.walk(target_path):
                    for file in files:
                        full_path = Path(root) / file
                        rel = full_path.relative_to(target_path.parent)
                        zf.write(full_path, arcname=str(rel))
            else:
                zf.write(target_path, arcname=f"kira-calculator/{target_path.name}")

            readme = ROOT / "README.md"
            if readme.exists():
                zf.write(readme, arcname="README.md")
            license_file = ROOT / "LICENSE"
            if license_file.exists():
                zf.write(license_file, arcname="LICENSE")

    checksum = sha256_file(archive_path)
    checksum_file = archive_path.parent / f"{archive_path.name}.sha256"
    checksum_file.write_text(f"{checksum}  {archive_name}\n")
    print(f"Archive SHA256: {checksum} -> {checksum_file.name}")
    return archive_path


def package_archive(target_path: Path, version: str | None = None) -> Path:
    """Package platform-specific release archive with checksum."""
    system = platform.system().lower()
    if system == "linux":
        return package_tarball(target_path, version=version)
    elif system == "windows":
        return package_zip_windows(target_path, version=version)
    elif system == "darwin":
        return package_zip_macos(target_path, version=version)
    else:
        return package_tarball(target_path, version=version)


def package_appimage(binary_path: Path, version: str | None = None) -> Path | None:
    """Create a standalone AppImage for Linux."""
    appimagetool = PACKAGING / "tools" / "appimagetool"
    if not appimagetool.exists():
        system_appimagetool = shutil.which("appimagetool")
        if system_appimagetool:
            appimagetool = Path(system_appimagetool)
        else:
            print("Note: packaging/tools/appimagetool not found; skipping AppImage build.")
            return None

    ver = version or get_project_version()
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

    appimage_name = f"kira-calculator-{ver}-x86_64.AppImage"
    appimage_path = DIST / appimage_name

    cmd = [
        str(appimagetool),
        "--appimage-extract-and-run",
        "--no-appstream",
    ]
    runtime_file = PACKAGING / "tools" / "runtime-x86_64"
    if runtime_file.exists():
        cmd.extend(["--runtime-file", str(runtime_file)])
    cmd.extend([str(app_dir), str(appimage_path)])

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
    parser.add_argument(
        "--get-version",
        action="store_true",
        help="Print project version from pyproject.toml and exit",
    )
    parser.add_argument(
        "--check-tag",
        type=str,
        default="",
        help="Validate that a git tag string matches the project version",
    )
    build_mode = parser.add_mutually_exclusive_group()
    build_mode.add_argument(
        "--onefile",
        dest="onefile",
        action="store_true",
        help="Build a single standalone executable (default)",
    )
    build_mode.add_argument(
        "--onedir",
        dest="onefile",
        action="store_false",
        help="Build an application directory (required for macOS .app bundles)",
    )
    parser.set_defaults(onefile=True)
    parser.add_argument(
        "--archive",
        action="store_true",
        default=True,
        help="Create distributable archive for current platform",
    )
    parser.add_argument(
        "--tarball",
        action="store_true",
        default=False,
        help="Alias for --archive",
    )
    parser.add_argument(
        "--appimage",
        action="store_true",
        default=False,
        help="Create AppImage (Linux only if tools present)",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Do not clean build cache before building",
    )
    args = parser.parse_args()

    project_version = get_project_version()

    if args.get_version:
        print(project_version)
        return 0

    if args.check_tag:
        if not validate_tag(args.check_tag):
            clean_tag = args.check_tag.strip()
            if clean_tag.startswith("refs/tags/"):
                clean_tag = clean_tag[len("refs/tags/") :]
            if clean_tag.startswith("v"):
                clean_tag = clean_tag[1:]
            print(
                f"ERROR: Tag version '{clean_tag}' does not match pyproject.toml version '{project_version}'!",
                file=sys.stderr,
            )
            return 1
        print(f"SUCCESS: Tag '{args.check_tag}' matches project version '{project_version}'.")
        return 0

    print(
        f"=== Building Optimized Kira Calculator v{project_version} on {platform.system()} ({platform.machine()}) ==="
    )
    binary_path = build_pyinstaller(onefile=args.onefile, clean=not args.no_clean)

    if not binary_path.exists():
        print(
            f"ERROR: Build output {binary_path} was not created!",
            file=sys.stderr,
        )
        return 1

    size_mb = binary_path.stat().st_size / (1024 * 1024)
    print(f"\nSuccessfully built optimized binary: {binary_path} ({size_mb:.1f} MB)")

    if args.archive or args.tarball:
        package_archive(
            archive_target(binary_path, args.onefile),
            version=project_version,
        )

    if args.appimage and platform.system().lower() == "linux":
        package_appimage(binary_path, version=project_version)

    print("\nPackaging completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
