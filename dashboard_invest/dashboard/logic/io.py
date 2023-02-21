# native imports
import re

# 3rd party imports
import requests
from bs4 import BeautifulSoup as BS
import numpy as np

# pandas 
import pandas as pd
pd.options.mode.chained_assignment = None

# website URL
GSHEETS_URL = "https://docs.google.com/spreadsheets/d/" \
    "12-GISr1efphjtpuJLCfQzI2akNXxaJ1iabsG24ib71c/edit#gid=1755810028"

# GOOGLE DOCS IO
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

def get_sheet_ids(url: str, last_sheet_name: str) -> list[str]:
    """Return Gsheets ID's based on initial page url and last sheet name.

    Args:
        url (str): URL of the initial page.
        last_sheet_name (str): Name of the last sheet.

    Returns:
        list[str]: List of sheet ID-s as string.
    """

    # Send a GET request to the Google Sheets URL
    r = requests.get(url)

    # Create a BeautifulSoup object from the HTML content
    soup = BS(r.content, 'html.parser')
    
    # find <body> -> <script> -> sheet_names_pattern -> id_pattern
    pattern = re.compile(rf"topsnapshot.+{last_sheet_name}\\\"\]")
    sheet_ids = None
    for tag in soup.body.find_all('script'):
        
        if tag.string is not None:
            string = re.search(pattern, tag.text)
            if string is not None:
                sheet_ids = re.findall(r"\d{9,}", string[0])
                break
    
    # assert if first ID match matches the first sheet id from the url
    assert sheet_ids[0] == re.search(r"\d+?$", url)[0], "Gsheet ID's do not match with sheet names!"        
    
    return sheet_ids

def get_sheet_urls(url: str) -> dict:
    """Return dictionary of based on home url.

    Args:
        url (str): Home page URL.

    Returns:
        dict: Dict of {sheet_name:sheet_url}.
    """
    # match the base url w/o ending sheet ID
    base_url = re.match(r".*edit#gid=", url)[0]
    
    sheet_names = get_sheet_names(url)
    sheet_ids = get_sheet_ids(url, last_sheet_name=sheet_names[-1])
    
    # check that # of sheets equals # of found sheet IDs 
    assert len(sheet_names) == len(sheet_ids), "Number of sheets doesn't match with number of ID-s."
    
    # create a dictionary of sheet name : sheet_url
    sheet_urls = [base_url + sheet_id for sheet_id in sheet_ids]
    
    return {sheet_name: sheet_url for sheet_name,sheet_url in zip(sheet_names, sheet_urls)}

def read_gsheet(url:str, **read_csv_kwargs):
    """Read data from google sheets into DF."""
    
    # replace 'edit#gid' with 'export?format=csv&gid'
    url_csv = url.replace("edit#gid", "export?format=csv&gid")
    return pd.read_csv(url_csv, **read_csv_kwargs)


### DATAFRAME IO ###
def findRefRowCol(df: pd.DataFrame, pattern: str, method: str='contains') -> tuple[int, int]:
    """Find reference row and column numeric index values.

    Args:
        pattern (str): Character sequence or regular expression.
        method (str, optional): Finding reference via pattern within the text ('contains')
            or equalling the value exactly ('equals'). Defaults to 'contains'.

    Raises:
        ValueError: Raises error if other than ['contains', 'equals'] is specified for the method.

    Returns:
        tuple[int, int]: Tuple of ['row_i', 'col_i']
    """
    
    
    # validate that method is correctly entered
    if method not in ['contains', 'equals']:
        raise ValueError(f"{method} can take only values: 'contains' or 'equals'!")
    
    idx_series = None
    if method == 'contains':
        idx_series = df.apply(lambda x: x.str.contains(pattern)).idxmax()
    if method == 'equals':
        idx_series = (df == pattern).idxmax()
    
    return idx_series.max(), idx_series.idxmax() 
    
def sliceDF(df: pd.DataFrame, 
            row_idx1: int=None, 
            row_idx2:int=None, 
            col_idx1: int=None, 
            col_idx2: int=None,
            col_0: bool=True, 
            direction='down') -> pd.DataFrame:
    """Slice DF till the first occuring empty row in given direction.

    Args:
        col_0 (bool, optional): If col_idx1 is actually first column. Defaults to True.
        direction (str, optional): Slice upwards or downwards from given row index. Defaults to 'down'.

    Raises:
        ValueError: If no row indices are specified.

    Returns:
        pd.DataFrame
    """
    
    # assert that at least one of the row indices is specified
    if row_idx1 is None and row_idx2 is None:
        raise ValueError(f"Both row indices can't equal {None}!") 
    
    # if column index is not the first column then None
    col_idx1 = col_idx1 if col_0 is True else None
    
    # find missing row index
    if direction == 'down':
        nan_mask = (df.iloc[row_idx1:,col_idx1:col_idx2] == 'nan').all(axis='columns')
        row_idx2 = None if nan_mask.sum() == 0 else nan_mask.idxmax()
        
    
    if direction == 'up':
        nan_mask = (df.iloc[:row_idx2,col_idx1:col_idx2] == 'nan').all(axis='columns')
        row_idx1 = None if nan_mask.sum() == 0 else nan_mask[::-1].idxmax() + 1
        row_idx2 += 1
         
    return df.iloc[row_idx1:row_idx2,col_idx1:col_idx2]

def getDFs(df: pd.DataFrame, references_dict: dict[str, tuple[str,str,str]]) -> dict[str, pd.DataFrame]:
    """Get subset DFs from a bigger DF based on reference strings.

    Args:
        df (pd.DataFrame): Raw initial DF.
        references_dict (dict): Dictionary of df_name: tuple('method', 'string' , 'direction').
            method has 2 options ['contains' and 'equals'], 'direction' has 3 options 
            ['one', 'down', 'up'] where one means only one line needs to be parsed, 'up' and 'down'
            respectively correspond to the parsing direction from the reference point.
            
            Returns:
        dict: Dictionary of {'df_name': df}
    """
    
    
    # set all cols str type, NaN -> 'nan'
    df = df.reset_index(drop=True).astype(str)
    
    # find reference indices
    dfs = {}
    for k,v in references_dict.items():
        
        row_i, col_i = findRefRowCol(df, pattern=v[1], method=v[0])
        col_i = 0 if k=='risk' else col_i
        
        if v[2] == 'one':
            dfs[k] = df.iloc[row_i,col_i:]
        if v[2] == 'down':
            dfs[k] = sliceDF(df, row_idx1=row_i, col_idx1=col_i, direction=v[2])
        if v[2] == 'up':
            dfs[k] = sliceDF(df, row_idx2=row_i, col_idx1=col_i, direction=v[2])

    # strip all NaN cols and rows
    dfs_clean = {}
    for k,df_ in dfs.items():
        
        if isinstance(df_, pd.Series):
            dfs_clean[k] = (df_
            .replace({'nan': np.nan})
            .dropna(how='any', axis='rows')
            )
        else:
            dfs_clean[k] = (df_
                .replace({'nan': np.nan})
                .dropna(how='all', axis='columns')
                .dropna(how='all', axis='rows')
            )
    
    return dfs_clean


### DF MODIFICATION ###
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