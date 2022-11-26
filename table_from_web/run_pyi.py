#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 09:22:07 2022

@author: tonu
"""
import os
from PyInstaller.config import CONF

CONF['workpath'] = os.getcwd()
CONF['spec'] = 'main.spec'

from PyInstaller.__main__ import run
from PyInstaller.building.datastruct import TOC, Tree
from PyInstaller.building.build_main import Analysis
from PyInstaller.building.api import EXE, PYZ, COLLECT, PKG, MERGE

datas = [('libs/uix/kv/webtable_screen.kv', 'libs/uix/kv')]

block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['libs.uix.baseclass.webtable_screen', 'libs.uix.kv', 'libs.uix', 
    'libs.logic'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['numpy', 'scipy', 'matplotlib'],
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
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)