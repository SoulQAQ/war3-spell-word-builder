# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 打包配置文件
PyQt EXE Template
"""

import os
import sys
from pathlib import Path

# 项目根目录
project_root = os.path.abspath('.')

a = Analysis(
    ['script\\main.py'],
    pathex=[project_root],
    binaries=[],
    datas=[
        ('resources', 'resources'),
        ('config', 'config'),
        ('app.ico', '.'),
        ('logo.png', '.'),
    ],
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.sip',
        'yaml',
        'requests',
        'urllib3',
        'charset_normalizer',
        'idna',
        'certifi',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'cv2',
        'IPython',
        'jupyter',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='pyqt-exe-template',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI 程序不显示控制台
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['app.ico'] if os.path.exists('app.ico') else None,
)
