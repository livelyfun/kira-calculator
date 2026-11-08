#!/usr/bin/env python3
"""Automated script to capture pixel-accurate UI screenshots for verification and documentation."""

import os
from pathlib import Path

# Configure headless offscreen rendering
os.environ["QT_QPA_PLATFORM"] = "offscreen"

from kira_calculator.app import create_application
from kira_calculator.ui.themes import apply_theme

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "docs" / "screenshots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def capture_all():
    app, window = create_application()
    window.show()

    # Populate some initial history entries
    window.history_service.add_entry("128 * 64", "8192", "Standard")
    window.history_service.add_entry("sin(30) + cos(60)", "1", "Scientific")
    window.history_service.add_entry("sqrt(1024) * 2", "64", "Standard")
    window.history_drawer.refresh()

    screenshots = [
        ("standard_dark.png", "Standard", "dark", 720, 600, False, "1337 + 42", "1379"),
        ("scientific_dark.png", "Scientific", "dark", 780, 640, False, "sin(45)^2 + cos(45)^2", "1"),
        ("programmer.png", "Programmer", "dark", 780, 640, False, "", ""),
        ("converter.png", "Converter", "dark", 720, 600, False, "", ""),
        ("standard_light.png", "Standard", "light", 720, 600, False, "2.5 * 4", "10"),
        ("history_open.png", "Standard", "dark", 840, 600, True, "128 * 64 =", "8192"),
        ("compact_window.png", "Standard", "dark", 480, 520, False, "7 * 8", "56"),
        ("large_window.png", "Scientific", "dark", 1280, 800, True, "sqrt(256) * 4", "64"),
    ]

    for filename, mode, theme, w, h, show_history, expr, res in screenshots:
        apply_theme(app, theme)
        window.nav_bar.set_theme_choice(theme)
        window.set_mode(mode)
        window.resize(w, h)
        window._set_history_visible(show_history)

        if mode in ("Standard", "Scientific"):
            window.display.set_expression(expr)
            window.display.set_result(res)

        app.processEvents()

        # Capture pixmap
        pixmap = window.grab()
        target_file = OUTPUT_DIR / filename
        pixmap.save(str(target_file))
        print(f"Captured: {target_file} ({pixmap.width()}x{pixmap.height()})")

    print("\nAll 8 release verification screenshots captured successfully.")


if __name__ == "__main__":
    capture_all()

