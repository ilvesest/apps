#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 16:55:30 2022

@author: tonu
"""

import os

from kivy.lang import Builder


def load_kv(file_name: str, file_path=os.path.join("libs", "uix", "kv")):
    """
    Load .kv file into corresponding Builder.

    Parameters
    ----------
    file_name : str
        Name of the .kv file to be read in.
    file_path : str
        Join path structure intelligently where .kv resides. The default is 
        os.path.join("libs", "uix", "kv").

    Returns
    -------
    None.

    """
    Builder.load_file(os.path.join(file_path, file_name))
