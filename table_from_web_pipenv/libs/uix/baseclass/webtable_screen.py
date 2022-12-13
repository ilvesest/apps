#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 17:38:49 2022

@author: tonu
"""

import utils
import os
import pandas as pd


from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty, ObjectProperty
from libs.logic.helpers import read_html_tables
from libs.logic.constants import WEB_URL

import tkinter as tk
from tkinter import filedialog


# load in .kv file
utils.load_kv("webtable_screen.kv")


class MainWidget(GridLayout):
    
    # url properties
    url_str = StringProperty(WEB_URL) # user input url
    read_url_dct = {"df_list": [], "message": ""}
    message_text = StringProperty("")

    
    # tables properties
    n_tables = ObjectProperty(0)
    first_table_idx = StringProperty("0")
    
    # nth table properties
    nth_table = ObjectProperty(None)
    nth_table_str = StringProperty("")
    
    # browse button
    table_file_path = StringProperty(os.path.join(os.getcwd(), 
        f"Table_{nth_table}.csv"))
    browse_str = StringProperty("")
    
    # selected DF
    df = None
    
    def validate_url_text(self, widget):
        self.url_str = widget.text
        self.read_url_dct = read_html_tables(self.url_str)
        self.message_text = self.read_url_dct['message']
        self.n_tables = len(self.read_url_dct['df_list'])
        if self.n_tables >= 1: self.first_table_idx = "1"
    
    def validate_nth_table_text(self, widget):
        self.nth_table = int(widget.text)
        self.nth_table_str = f"Table {self.nth_table} chosen."
        self.df = self.read_url_dct['df_list'][self.nth_table - 1]
        
    def tk_browse(self):
        # open OS native file browser
        root = tk.Tk()
        root.withdraw()
        file = filedialog.asksaveasfilename(
            filetypes=[('csv file', '.csv'), ('excel file', '.xlsx')],
            defaultextension=".csv",
            initialfile=f"Table_{self.nth_table}")
        if file:
            self.df.to_csv(file, index=False)
            self.browse_str = f"File successfully saved."
    
# class PathButton(Button):
    
#     table_file_path = MainWidget().table_file_path
    
#     @staticmethod
#     def get_path(self):
#         root = tk.Tk()
#         root.withdraw()
#         self.table_file_path = filedialog.askdirectory()
         
        
    

