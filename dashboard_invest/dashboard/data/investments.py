# local imports
from dashboard.logic.io import GSHEETS_URL, read_gsheet, df_add_button
from dashboard.logic.plots import components, pie_chart, cdn_js

# 3rd party imports
import pandas as pd

# Summary DF
df = read_gsheet(
    GSHEETS_URL, 
    header=None, 
    usecols=[0,1,2], 
    nrows=11,
    names=['Asset Class', 'Total Value', 'Comments']
).dropna(how='all')

# convert comment to a button
df.Comments[df.Comments.notna()] = df.Comments[df.Comments.notna()].apply(df_add_button)
df = df.fillna("") # convert NaN-s to ""

df_style = df.copy()

# style df for table
df_style = df_style.style \
    .set_properties(
        subset=pd.IndexSlice[df.query("`Asset Class` == 'Total (USD)'").index, :], 
        **{"color": "#E2B842"}) \
    .set_properties(
        subset=pd.IndexSlice[df.query("`Asset Class` == 'Monthly Income'").index, :], 
        **{"color": "grey"}) \
    .hide(axis='index')

total_investments_df = df_style

# modify df for PIE-CHART
df_plot = df.copy()
df_plot = df_plot.query("`Asset Class` != 'Monthly Income' & `Total Value` != '#ERROR!'")
df_plot = df_plot.drop("Comments", axis='columns')
df_plot['Total Value'] = df_plot['Total Value'].replace(r"[\$,]", "", regex=True).astype(float)
df_plot.columns = df_plot.columns.map(lambda x: x.replace(" ", "_"))


pie_chart_plot = pie_chart(
    df=df_plot,
    x='Asset_Class',
    y='Total_Value')

plot_js, plot_div = components(pie_chart_plot)
