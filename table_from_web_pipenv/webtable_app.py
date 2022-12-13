#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 16:46:57 2022

@author: tonu
"""

from kivy.app import App
from kivy.factory import Factory



class WebTable(App):

    def build(self):
        Factory.register('MainWidget', 
                         module="libs.uix.baseclass.webtable_screen")
        Factory.register('PathButton',
                         module="libs.uix.baseclass.webtable_screen")
        return Factory.MainWidget()
