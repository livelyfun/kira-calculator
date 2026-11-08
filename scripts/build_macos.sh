#!/usr/bin/env bash
# macOS packaging helper for Kira Calculator
set -euo pipefail

APP_NAME="Kira Calculator"
VERSION="1.0.0"
DIST_DIR="dist"

echo "=== Building macOS bundle for ${APP_NAME} v${VERSION} ==="

python3 scripts/build_app.py --onefile

if [[ -f "${DIST_DIR}/kira-calculator" ]]; then
    echo "Binary built: ${DIST_DIR}/kira-calculator"
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
echo "  xcrun notarytool submit dist/kira-calculator.zip --keychain-profile \"...\" --wait"

