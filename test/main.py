#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 10:05:51 2022

@author: tonu
"""

import os
import sys

# root_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
# sys.path.insert(0, os.path.join(root_dir, "libs", "data"))
# sys.path.insert(0, os.path.join(root_dir, "libs", "uix"))


from libs.uix.base.helper import load_csv
from libs.uix.utils import read_csv


if __name__ == '__main__':
    load_csv()
    read_csv()
    