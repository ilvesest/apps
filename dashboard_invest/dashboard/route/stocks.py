# local imports
from dashboard.logic.constants import nav_names
from dashboard.logic.io import read_gsheet, getDFs, findRefRowCol, comment_button

# 3rd party imports
import pandas as pd

STOCKS_URL = nav_names['Stocks']['url']


# read spreadsheet in as DF
df_stocks_raw = read_gsheet(url=STOCKS_URL, header=None)

# extract data into sub DF-s
references_dict = {
    'stocks' : ("equals", "Company", "down"),
    'analysis' : ("contains", "Analysis ratio", "down"),
    'sectors1' : ("contains", "S&P500 Index", "down"),
    'sectors2' : ("contains", "Don't just buy crap! ", "up", 0)
}
df_dict_stocks = getDFs(df_stocks_raw, references_dict)

### STOCKS TABLE ###
df_stocks = df_dict_stocks['stocks'].copy().reset_index(drop=True)

# set column headers
df_stocks.columns = df_stocks.iloc[0]
df_stocks = df_stocks.iloc[1:].reset_index(drop=True)

# check if df is empty and if so is there extra info
all_nan = df_stocks.iloc[:,1:].isna().all(axis=1)
all_nan_idx = all_nan.loc[all_nan].index

df_stocks_info = df_stocks.loc[all_nan].dropna(axis='columns') # info
df_stocks = df_stocks.loc[~df_stocks.index.isin(all_nan_idx),] # df stocks


### ANALYSIS RATIOS TABLE & TITLE ###
df_ana = df_dict_stocks['analysis'].copy()

# title of the analysis section
stocks_ana_title = df_ana.iloc[0,0]

# set header
header_idx = findRefRowCol(df_ana.astype('str'), r"Ratio:", 'contains')[0]
df_ana.columns = df_ana.loc[header_idx]
df_ana = df_ana.loc[header_idx+1:].reset_index(drop=True)
df_ana.columns = df_ana.columns.fillna('') # fill NaN headers ""

# Join column values using whitespace for columns with NaN header
df_ana = df_ana.fillna('')
joined_nan_cols = df_ana.loc[:, ""].apply(lambda x: "".join(x.astype(str)), axis=1)

# capture first nan column pos index
nan_col_idx = [i for i,col in enumerate(df_ana.columns) if col == ""][0]

# remove original nan columns
df_ana = df_ana.drop([''], axis='columns')
df_ana.insert(nan_col_idx, "Comment", joined_nan_cols)

# add comment button 
df_ana.Comment[df_ana.Comment != ''] = df_ana.Comment[df_ana.Comment != ''].apply(comment_button)
df_stocks_ana = df_ana


### SUGGESTED SECTORS
stock_sectors_title = "Suggested sectors for long term value"

df_sec1 = df_dict_stocks['sectors1'].copy().set_index(0)
df_sec2 = df_dict_stocks['sectors2'].copy().set_index(0)

# prepare sectors 1 table
df_sec1 = df_sec1 = df_sec1.apply(lambda x: x.str.strip())
tech_label_1 = df_sec1.index[df_sec1.index.str.contains(r"tech", case=False, regex=True)][0]

df_sec1 = (df_sec1
    .apply(lambda x: x.str.strip())
    .apply(lambda x: x+'.' if x[-1] not in ['.', '!', '?', '%', '>'] else x, axis="rows")
    .fillna("")
    .apply(lambda x: " ".join(x.astype(str)).strip(), axis=1)
)

# add empty index row entry to previous
if df_sec2.index.isna()[-1]:
    df_sec2.iloc[-2,-1] += ' ' + df_sec2.iloc[-1,-1]

# prepare sectors 2 table
df_sec2 = df_sec2.iloc[:-1,] # remove last row
tech_label_2 = df_sec2.index[df_sec2.index.str.contains(r"tech", case=False, regex=True)][0]
df_sec2 = df_sec2.rename(index={tech_label_2: tech_label_1})
df_sec2.columns = ['Proportion', 'Comment']

# join and modify tables
df_sectors = pd.concat([df_sec1, df_sec2], axis='columns')

df_sectors = (df_sectors
    .drop('Proportion', axis='columns')
    .apply(lambda x: x.str.strip())
    .apply(lambda x: x+'.' if x[-1] not in ['.', '!', '?', '%', '>'] else x, axis="rows")
    .fillna("")
    .apply(lambda x: " ".join(x.astype(str)).strip(), axis=1)
)

df_sectors = (pd.concat([df_sectors, df_sec2['Proportion']], axis='columns')
    .rename(columns={0: 'Comment'})
    .reset_index()
    .rename(columns={0: 'Sector'})
    .fillna("")
)

# add Details button to comments
df_sectors.Comment[df_sectors.Comment != ''] = \
    df_sectors.Comment[df_sectors.Comment != ''].apply(comment_button)