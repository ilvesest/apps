#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 19:53:55 2022

@author: tonu
"""



def read_csv():
    with open("libs/uix/kv/simpsons3.csv", 'r') as file:
        lines = file.readlines()
        print('\n' + lines[8])
        