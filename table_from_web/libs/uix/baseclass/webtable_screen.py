#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 17:38:49 2022

@author: tonu
"""

import utils

from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty


# load in .kv file
utils.load_kv("webtable_screen.kv")


class MainWidget(GridLayout):
    
    url_str = StringProperty()
    def on_text_validate(self, widget):
        self.url_str = widget.text
        print(self.url_str)
    