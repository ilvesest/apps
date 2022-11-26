#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 18:11:12 2022

@author: tonu
"""

from PyInstaller.utils.hooks import collect_submodules, collect_data_files
from PyInstaller.utils.hooks import conda_support


conda_support.collect_dynamic_libs()

datas = collect_data_files('libs')
print(datas)
# hiddenimports = collect_submodules('./bump')
# print(hiddenimports)
