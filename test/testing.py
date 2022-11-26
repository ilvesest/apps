#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 08:07:11 2022

@author: tonu
"""

from PyInstaller.utils.hooks import collect_data_files


print(collect_data_files('libs', subdir='uix/kv', includes=['*.csv']))