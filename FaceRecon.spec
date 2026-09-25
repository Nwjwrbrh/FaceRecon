# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path
import sqlite_vec

sqlite_vec_dir = Path(sqlite_vec.__file__).resolve().parent

if sys.platform == "win32":
    vec_binary = sqlite_vec_dir / "vec0.dll"
elif sys.platform == "darwin":
    vec_binary = sqlite_vec_dir / "vec0.dylib"
else:
    vec_binary = sqlite_vec_dir / "vec0.so"


a = Analysis(
    ['src/main.py'],
    pathex=[],

    binaries=[
        (str(vec_binary), 'sqlite_vec'),
    ],

    datas=[
        ('assets/', 'assets'),
        ('model/','model'),
    ],

    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)


pyz = PYZ(a.pure)


exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='FaceRecon',

    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,

    disable_windowed_traceback=False,
    argv_emulation=False,

    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)


coll = COLLECT(
    exe,
    a.binaries,
    a.datas,

    strip=False,
    upx=True,
    upx_exclude=[],

    name='FaceRecon',
)
