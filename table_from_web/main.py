#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 20:39:36 2022

@author: tonu
"""

import os
import sys

# include project folders to path without __init__.py file
root_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.join(root_dir, "libs", "logic"))
sys.path.insert(0, os.path.join(root_dir, "libs", "uix"))


from webtable_app import WebTable


if __name__ == '__main__':
    WebTable().run()
