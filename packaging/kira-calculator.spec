# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules, collect_data_files
from pathlib import Path

block_cipher = None
project_root = Path.cwd()

# Core application data
datas = [
    (str(project_root / 'src' / 'kira_calculator' / 'ui' / 'themes'), 'kira_calculator/ui/themes'),
    (str(project_root / 'assets' / 'icons'), 'assets/icons'),
]

# Only include required PySide6 submodules and data
hiddenimports = [
    'PySide6.QtCore',
    'PySide6.QtGui',
    'PySide6.QtWidgets',
    'kira_calculator',
    'kira_calculator.app',
    'kira_calculator.core',
    'kira_calculator.modes',
    'kira_calculator.services',
    'kira_calculator.ui',
]

# Explicit exclusions of heavy unused modules
excludes = [
    # Massive unused Qt modules
    'PySide6.QtWebEngineCore',
    'PySide6.QtWebEngineWidgets',
    'PySide6.QtWebEngineQuick',
    'PySide6.Qt3DAnimation',
    'PySide6.Qt3DCore',
    'PySide6.Qt3DExtras',
    'PySide6.Qt3DInput',
    'PySide6.Qt3DLogic',
    'PySide6.Qt3DRender',
    'PySide6.QtQuick',
    'PySide6.QtQuick3D',
    'PySide6.QtQuickControls2',
    'PySide6.QtQuickTest',
    'PySide6.QtQuickWidgets',
    'PySide6.QtQml',
    'PySide6.QtMultimedia',
    'PySide6.QtMultimediaWidgets',
    'PySide6.QtBluetooth',
    'PySide6.QtPositioning',
    'PySide6.QtSensors',
    'PySide6.QtSerialPort',
    'PySide6.QtSerialBus',
    'PySide6.QtWebSockets',
    'PySide6.QtWebView',
    'PySide6.QtPdf',
    'PySide6.QtPdfWidgets',
    'PySide6.QtSpatialAudio',
    'PySide6.QtNfc',
    'PySide6.QtRemoteObjects',
    'PySide6.QtScxml',
    'PySide6.QtTextToSpeech',
    'PySide6.QtCharts',
    'PySide6.QtDataVisualization',
    'PySide6.QtGraphs',
    'PySide6.QtHttpServer',
    'PySide6.QtLocation',
    'PySide6.QtNetworkAuth',
    'PySide6.QtVirtualKeyboard',
    # Unused third-party libraries
    'tkinter',
    'matplotlib',
    'numpy',
    'scipy',
    'asteval',
    'pytest',
    'ruff',
]

a = Analysis(
    ['src/kira_calculator/__main__.py'],
    pathex=['src'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='kira-calculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icons/kira-calculator.png',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='kira-calculator',
)
