# local imports
from dashboard.logic.io import GSHEETS_URL, read_gsheet, comment_button, total_assets, \
    total_value_to_num, getDataFrames
from dashboard.logic.plots import components, pie_chart, cdn_js

# 3rd party imports
import pandas as pd
import numpy as np

# Read in summary DF and drop empty rows
df = read_gsheet(
    GSHEETS_URL, 
    header=None
)

# Extract sub DF to dictionary
df_dict = getDataFrames(df)

# ADS
df_ads = df_dict['ads'].copy()
df_ads.columns = ['text', 'hyperlink']
df_ads['icon'] = df_ads.text.str[:1]
df_ads['text'] = df_ads.text.str[2:]
headers = ['Course', 'Mentoring', 'PM Global', 'PM USA', 'PM UK', 'Crypto Security', 'Stock Platform', 'Bank Account']
df_ads['header'] = headers

## Main DF ##
df_table = df_dict['main']
df_table.columns = ['Asset Class', 'Total Value', 'Comments']
df_table = df_table.set_index('Asset Class')

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

# variable for the routes.py
styler_main = df_style

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

# ASSET RISKS
df_risk = df_dict['risk'].copy()
df_risk = df_risk.iloc[1:-5]
df_risk.columns = ['asset', 'risk', 'comment']
df_risk.iloc[-2].comment += ". " + df_risk.iloc[-1, -1]
df_risk = df_risk.iloc[:-1].reset_index(drop=True)
df_risk['risk'] = [1, 1, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4]
df_risk['risk_word'] = df_risk['risk'].replace({1:'VERY LOW', 2: 'LOW', 3: 'MEDIUM', 4: 'HIGH'})
df_risk['li_group'] = df_risk['risk'].replace({1: 'success', 2: 'warning', 3: 'info', 4: 'danger'})

# ANNOUNCEMENTS
df_a = df_dict['announcements'].copy()
df_a = df_a.reset_index(drop=True)
df_a = df_a[0].str.split(pat=':', n=1, expand=True)
df_a.columns = ['date', 'text']
df_a.loc[df_a[df_a['date'] == 'Post to Patreon'].index[0], 'date'] = 'Jan 2023'
df_a['heading'] = ['Property Purchase', 'Rising Rates', 'Stocks Ralley and Crash', 
                   'No Change', 'Assets Falling', 'Cash is King', 'Stockbiling Cash', 
                   'Accumulating Cash', 'Into Cash!']


# GENERAL ADVICE
df_advice = df_dict['advice'].copy()
df_advice = df_advice.reset_index(drop=True)

# GENERAL NOTES
df_gen = df_dict['general_notes'].copy()
df_suc = df_dict['success'].copy()

df_suc.iloc[0, 1] = df_suc.iloc[0, 1] + df_suc.iloc[-1,1]
df_gen = pd.concat([df_gen.iloc[1:], df_suc.iloc[0,:].to_frame().T]).reset_index(drop=True)
df_gen.columns = ['field', 'info']

# HISTORICAL INVESTMENTS
df_hist = df_dict['historical'].copy()
df_hist = df_hist.reset_index(drop=True)



