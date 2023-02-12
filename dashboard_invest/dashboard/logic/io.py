# 3rd party imports
import requests
from bs4 import BeautifulSoup as BS

# pandas 
import pandas as pd
pd.options.mode.chained_assignment = None

# website URL
GSHEETS_URL = "https://docs.google.com/spreadsheets/d/" \
    "12-GISr1efphjtpuJLCfQzI2akNXxaJ1iabsG24ib71c/edit#gid=1755810028"

# Google Docs related IO
def get_sheet_names(url: str, class_name: str="goog-inline-block docs-sheet-tab-caption") -> list[str]:
    """Find all Google Spreadsheet Sheet names

    Args:
        url (str): URL to the Google Spreadhseet
        class_name (str, optional): Tag's 'class' name to search for that contains sheet names. 
            Defaults to "goog-inline-block docs-sheet-tab-caption".

    Returns:
        list[str]: List of sheet names.
    """
    # create soup object
    soup = BS(requests.get(url).text, features="html.parser")
    
    # find all sheet raw tags as list
    sheet_tags = soup.find_all(name="div", attrs={"class": class_name})
    
    return [tag.contents[0] for tag in sheet_tags]


def read_gsheet(url:str, **read_csv_kwargs):
    """Read data from google sheets into DF."""
    
    # replace 'edit#gid' with 'export?format=csv&gid'
    url_csv = url.replace("edit#gid", "export?format=csv&gid")
    return pd.read_csv(url_csv, **read_csv_kwargs)


### DATAFRAME MODIFICATION ###
def findRowColRegex(df: pd.DataFrame, pat: str, case: bool=True, regex:bool=True):
    """Return subset DF beginning index and col tuple

    Args:
        df (pd.DataFrame): DF to be subset.
        pat (str): Regex pattern to be search for.
        case (bool, optional): Case sensitive. Defaults to True.
        regex (bool, optional): If pattern treated like regex or not. Defaults to True.

    Raises:
        ValueError: If 0 pattern matches are found.
        ValueError: If more than pattern matches are found.

    Returns:
        tuple(row, col): Tuple of (row, col) values for the pattern match.
    """
    # make sure only one such pat exists in the df
    df_mask = df.apply(lambda x: x.str.contains(pat, case=case, regex=regex) if x.dtype == 'object' else None)
    
    count = df_mask.sum().sum()
    
    if count < 1: 
        raise ValueError(f'Given {pat} did not give any results.')
    if count > 1:
        raise ValueError(f'Given {pat} gave more than 1 results.')
     
    # col and row values where pat
    row = df_mask.any(axis='columns').argmax()
    col = df_mask.any(axis='index').argmax()
    
    return row, col

def getDataFrames(df: pd.DataFrame):
    """Divide big DF into sub DFs based on patterns and empty rows.

    Args:
        df (pd.DataFrame): DF.

    Returns:
        dict{'df_name': df}: Dictionary of DFs with their respective names as keys.
    """
    
    df = df.reset_index(drop=True)
    dataframes_dict = {}
    
    # MAIN DF
    main_df_idx2 = (df == 'Monthly Income').any(axis='columns').argmax()
    dataframes_dict['main'] = df.iloc[:main_df_idx2+1,:3].dropna(how='all', axis='rows')
    
    # ADS DF
    r1, c1 = findRowColRegex(df, "My Finance Course")
    
    
    ads_df = df.iloc[r1:,c1:].reset_index(drop=True)
    ads_df = (ads_df
        .loc[:(ads_df[c1].isna()).argmax()-1, :]
        .dropna(how='all', axis='columns')
    )
    dataframes_dict['ads'] = ads_df
    
    # OTHER DFS
    df_names = [
    'announcements',
    'advice',
    'error_warning',
    'risk',
    'skip',
    'skip',
    'skip',
    'historical',
    'cash_pos',
    'general_notes',
    'success',
    ]
    
    # Find rows after main df where all values are NaN-s.
    nan_rows = df.iloc[main_df_idx2+1:,].isna().all(axis='columns')
    
    # Indices where all NaN-s in the row
    dfs_idxs = []
    
    for i,bool in nan_rows.items():
        
        if i == nan_rows.index[-1]:
            dfs_idxs.append(None)
            break
        if bool:
            dfs_idxs.append(i)
    
    # raw dataframes
    dfs = []        
    for i,idx in enumerate(dfs_idxs):
        if i == len(dfs_idxs) - 1:
            break
        dfs.append(df.iloc[idx:dfs_idxs[i+1]])
    
    # strip dataframes from NaN-s and add to dictionary
    for df_, name in zip(dfs, df_names):
        
        if name == 'skip': continue
        
        dataframes_dict[name] = (df_
            .dropna(how='all', axis='columns')
            .dropna(how='all', axis='rows')
        )
    
    return dataframes_dict

def total_assets(df: pd.DataFrame, index:str, col:str) -> pd.DataFrame:
    """Calculate total value if '#ERROR!'
    """
 
    # check if total value has ERROR msg
    if df.loc[index, col] == "#ERROR!":
        df.loc[index, col] = 0
    else:
        return df.loc[index, col]
     
    # exclude error fields and monthly income
    df = df[(df[col] != '#ERROR!') & (df.index != 'Monthly Income')]
    
    # str to float and calc total sum
    df.loc[:, col] = df[col].replace(r"[\$,]", "", regex=True).astype(float)
    df.loc[index, col] = df[col].sum()
    
    # format numbers back to string
    return "${0:,.2f}".format(df.loc[index, col])

def comment_button(series:pd.Series) -> str:
    """Replaces value in the DF to given html.

    Args:
        sereis (pd.Series): pandas Series obj
        data : data

    Returns:
        str: Returns the html string
    """
    return f'<button type="button" class="btn btn-secondary btn-sm" data-bs-content="{series} '\
        '"data-bs-toggle="popover" data-bs-trigger="focus" '\
        'style="--bs-btn-font-size: .85rem">Details</button>'

def total_value_to_num(df: pd.DataFrame):
    """Modify DF data column to numeric
    """
    
    # add underscores to col names
    df.columns = df.columns.map(lambda x: x.replace(" ", "_"))
    
    # set 'Asset_Class' as new index
    df = (df
        .set_index('Asset_Class') 
        .drop('Comments', axis='columns')
        .loc[:'Total (USD)'].iloc[:-1]
        .query("Total_Value != '#ERROR!'")
    )
    
    df['Total_Value'] = pd.to_numeric(df['Total_Value'].replace(r"[\$,]", "", regex=True),
                                      errors='coerce')
    return df.reset_index()    