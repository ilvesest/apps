# local imports
from dashboard.logic.io import GSHEETS_URL, read_gsheet

# Summary DF
total_investments_df = read_gsheet(
    GSHEETS_URL, 
    header=None, 
    usecols=[0,1,2], 
    nrows=11,
    names=['Asset Class', 'Total Value', 'Comments']
).fillna("")

# 