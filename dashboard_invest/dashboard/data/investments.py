# local imports
from dashboard.logic.io import GSHEETS_URL, read_gsheet, add_button_df

# Summary DF
df = read_gsheet(
    GSHEETS_URL, 
    header=None, 
    usecols=[0,1,2], 
    nrows=11,
    names=['Asset Class', 'Total Value', 'Comments']
).dropna(how='all')

# convert comment to a button
df.Comments[df.Comments.notna()] = df.Comments[df.Comments.notna()].apply(add_button_df)

total_investments_df = df