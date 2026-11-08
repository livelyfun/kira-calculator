#!/usr/bin/env bash
# macOS packaging helper for Kira Calculator
set -euo pipefail

APP_NAME="Kira Calculator"
VERSION=$(python3 scripts/build_app.py --get-version)
DIST_DIR="dist"

echo "=== Building macOS bundle for ${APP_NAME} v${VERSION} ==="

python3 scripts/build_app.py --onefile --archive

if [[ -d "${DIST_DIR}/kira-calculator.app" || -f "${DIST_DIR}/kira-calculator" ]]; then
    echo "macOS build and archive complete in ${DIST_DIR}"
    # When running on macOS, create a .dmg if create-dmg is installed
    if command -v create-dmg >/dev/null 2>&1; then
        create-dmg \
            --volname "${APP_NAME}" \
            --window-pos 200 120 \
            --window-size 600 400 \
            "${DIST_DIR}/${APP_NAME}-${VERSION}.dmg" \
            "${DIST_DIR}/"
    fi
fi

echo "Note: For production distribution on macOS, sign and notarize with:"
echo "  codesign --deep --force --verify --verbose --sign \"Developer ID Application: ...\" dist/kira-calculator"
echo "  xcrun notarytool submit dist/kira-calculator-macos.zip --keychain-profile \"...\" --wait"
