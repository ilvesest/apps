# local imports
from dashboard.logic.io import GSHEETS_URL, read_gsheet, comment_button

# 3rd party imports
import pandas as pd    

STOCKS_WATCH_URL = "https://docs.google.com/spreadsheets/d/12-GISr1efphjtpuJLCfQzI2akNXxaJ1iabsG24ib71c/edit#gid=845083323"

# Read in summary DF and drop empty rows
df = read_gsheet(
    STOCKS_WATCH_URL, 
    header=None
)

# find df header row index using regex pattern
header_idx = df.apply(lambda x: x.str.contains("Neil's Value", case=False)).any(axis='columns').argmax()

# separate disclaimer and df
df_disclaimer = df.iloc[:header_idx-1, 0]
df_watch = df.iloc[header_idx:,]

# DISCLAIMER DF
df_disc = df_disclaimer.copy()

# add period end of the sentence if not so
df_disc = df_disc.to_frame().rename(columns={0: 'info'})
df_disc.loc[:,'info'] = [x + '.' if x[-1] != '.' else x for x in df_disc['info']]

# add color column and set it as cat for ordering purposes
df_disc['color'] = ['warning', 'success', 'warning', 'success', 'success', 'danger']
df_disc['color'] = pd.Categorical(df_disc['color'],
                                  categories=['success', 'warning', 'danger'],
                                  ordered=True)

# add icon_id column
icon_dict = {'warning': 'exclamation-triangle-fill', 'success': 'check-lg', 'danger':'exclamation-octagon-fill'}
df_disc['icon_id'] = df_disc['color'].map(icon_dict)
df_disc = df_disc.sort_values('color')

# STOCKS DF
# set first row as header & reset row idxs
df_watch.columns = df_watch.iloc[0].values
df_watch = df_watch.iloc[1:].reset_index(drop=True)

# Generate buttons for 'Notes' column
df_watch.Notes[df_watch.Notes.notna()] = df_watch.Notes[df_watch.Notes.notna()].apply(comment_button)
df_watch = df_watch.fillna("")

# Color Ratings based on category
rating_colormap = {'Sig Undervalued':'success', 'Mod Undervalued':'info', 'Fair Value':'light', 'Value Trap?':'danger'}

df_style = df_watch.style
for k,v in rating_colormap.items():
    df_style.set_properties(
        subset=pd.IndexSlice[df_watch.query(f"Rating == '{k}'").index, 'Rating'], 
        **{"color":f"var(--bs-{v}-text)", "background":f"var(--bs-{v}-bg-subtle)", "opacity": "1"})
    
df_style = df_style.hide(axis='index').set_table_attributes('class="stockwatch"')


    
    