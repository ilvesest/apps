#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 20:39:36 2022

@author: tonu
"""

import pandas as pd
from logic import constants as c

df_tables = pd.read_html(io=c.TEST_URL)

print(df_tables[2].head(3))