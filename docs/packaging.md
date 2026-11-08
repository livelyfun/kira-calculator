# Packaging and Releases

## Public downloads

Published binaries are distributed through [GitHub Releases](https://github.com/livelyfun/kira-calculator/releases). The CI workflow builds on native GitHub-hosted Linux, Windows, and macOS runners. A version tag matching `v*` (for example, `v1.0.1`) runs linting, the test matrix, and packaging. Only when all required jobs succeed does the workflow create a GitHub Release and attach the platform assets.

GitHub Actions workflow artifacts from ordinary branch builds are temporary CI artifacts, not permanent public downloads.

## Release assets

| Platform | Asset |
| --- | --- |
| Linux x86_64 | `kira-calculator-<version>-linux-x86_64.tar.gz` plus SHA256 file |
| Windows x64 | `kira-calculator-windows-x64.zip` |
| macOS | `kira-calculator-macos.zip` |
| All assets | `SHA256SUMS.txt` |

The Linux archive contains the standalone executable under `bin/kira-calculator`, along with the desktop entry, icon, README, and license when those source assets are present. The AppImage is not currently built in CI: the repository does not include the AppImage tooling/runtime required by the local AppImage packaging path.

## Build locally

Install the packaging extra and build on the target operating system:

```bash
python -m pip install -e ".[packaging]"

# Linux and Windows
python scripts/build_app.py --onefile

# macOS
python scripts/build_app.py --onedir
```

The packaging extra installs PyInstaller and Pillow; Pillow lets PyInstaller convert the source PNG into the native ICO/ICNS icon used by Windows and macOS builds. On Linux and Windows the script creates a single-file executable. On macOS it creates `dist/kira-calculator.app`, a onedir application bundle, and ZIPs the complete bundle together with the README and license. Linux builds also create a compressed distribution archive and SHA256 sidecar.

## Release workflow

1. Update the project version in `pyproject.toml` before preparing a new version.
2. Push a version tag, for example `v1.0.1`.
3. GitHub Actions runs lint, tests across Python 3.10–3.13 on Linux/Windows/macOS, and native packaging.
4. If all jobs pass, the release job publishes the assets and a `SHA256SUMS.txt` manifest.

Do not publish a release from a tag until its source tree and version metadata represent the intended release.

## Platform notes

- **Linux:** x86_64 build from `ubuntu-latest`. The target machine must provide compatible system libraries for the Qt platform plugin.
- **Windows:** x64 executable in a ZIP archive. The executable is not currently code-signed.
- **macOS:** onedir `.app` application bundle in a ZIP archive. The build is not currently signed or notarized; Gatekeeper may show a warning.

The binaries bundle the application and Python/Qt dependencies through PyInstaller. Users do not need to install Python separately.

## Verification

The CI pipeline runs the test suite before packaging. Packaged binaries should additionally be smoke-tested on clean target operating systems before being described as independently verified. A successful build proves packaging completed; it does not by itself prove compatibility with every OS version or desktop environment.
