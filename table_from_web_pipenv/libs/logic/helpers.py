#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 20:12:01 2022

@author: tonu
"""

import pandas as pd
from pandas.errors import ParserError


def read_html_tables(url: str) -> list[pd.DataFrame]:
    """
    Read all given tables into a list in a given url address.

    Parameters
    ----------
    url : str
        Website address containing tables.

    Returns
    -------
    Tables : list[DataFrame], str
        Returns list of tables as DataFrames.

    """
    event_dct = {"df_list": [], "message": None}
    try:
        event_dct["df_list"] = pd.read_html(io=url)
    except ValueError as e:
        if str(e) == "No tables found":
            # FIX when invalid URL is given
            event_dct["df_list"] = []
            event_dct["message"] = "Given URL doesn't contain any tables."
    except Exception:
        # NEEDS MORE PRECISE IMPLEMENTATION IN THE FUTURE!!!!!
        event_dct["df_list"] = []
        event_dct["message"] = "Invalid URL given."

    else:
        event_dct["message"] = f"{len(event_dct['df_list'])} tables successfully loaded."
    return event_dct
