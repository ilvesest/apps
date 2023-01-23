# local imports
from dashboard.logic.io import GSHEETS_URL, read_gsheet, comment_button, total_assets, \
    total_value_to_num
from dashboard.logic.plots import components, pie_chart, cdn_js

# 3rd party imports
import pandas as pd
import numpy as np

# Read in summary DF and drop empty rows
df = read_gsheet(
    GSHEETS_URL, 
    header=None, 
    usecols=[0,1,2], 
    nrows=11,
    names=['Asset Class', 'Total Value', 'Comments']
).dropna(how='all')

### TRANSFORM DF ###

## Table ##
df_table = df.copy().set_index('Asset Class')

# if '#ERROR!' in Total (USD) recalculate the sum and assign
df_table.loc['Total (USD)', 'Total Value'] = total_assets(df_table, 'Total (USD)', 'Total Value')

# --------------------- Dummy Data -------------------- #
# # Checking if asset class has error
# df_table.loc['Business Equity', ['Total Value']] = '#ERROR!'

# convert comment to a button
df_table.Comments[df_table.Comments.notna()] = df_table.Comments[df_table.Comments.notna()].apply(comment_button)
df_table = df_table.fillna("").reset_index()

df_style = df_table.copy()

# style df for table
df_style = df_style.style \
    .set_properties(
        subset=pd.IndexSlice[df_table.query("`Asset Class` == 'Total (USD)'").index, :], 
        **{"color": "#E2B842"}) \
    .set_properties(
        subset=pd.IndexSlice[df_table.query("`Asset Class` == 'Monthly Income'").index, :], 
        **{"color": "grey"}) \
    .set_properties(
        subset=pd.IndexSlice[df_table.query("`Total Value` == '#ERROR!'").index, "Total Value"], 
        **{"color": "red", "opacity": "0.75"}) \
    .hide(axis='index')

total_investments_df = df_style

# modify df for PIE-CHART
df_plot = df_table.copy()
df_plot = total_value_to_num(df_plot)

pie_chart_plot = pie_chart(
    df=df_plot,
    x='Asset_Class',
    y='Total_Value',
    background_color='#2C2B2B'
)

plot_js, plot_div = components(pie_chart_plot)
