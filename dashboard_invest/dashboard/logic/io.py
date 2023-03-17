# native imports
import re, datetime, os, traceback
from functools import wraps
from typing import Callable

# 3rd party imports
import requests
from bs4 import BeautifulSoup as BS
import numpy as np
import openpyxl

# pandas 
import pandas as pd
pd.options.mode.chained_assignment = None



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

def downloadWorkbook(spreadsheet_url: str, 
                     file_path: str,
                     file_name: str='workbook') -> None:
    """Download Google Spreadsheet as an .xlsx file.
    """
    
    # Define the file name and extension
    file_ext = ".xlsx"

    # Generate a timestamp string in the format YYYY-MM-DD_HH-MM-SS
    timestamp = getTimestamp()

    # Concatenate the timestamp string with the file name and extension
    timestamped_file_name = f"{file_path}/{timestamp}_{file_name}{file_ext}"

    # SAVE GOOGLE SPREADSHEET AS .XLSX FILE
    export_url = spreadsheet_url.replace("edit#gid", "export?format=xlsx")

    response = requests.get(export_url)

    with open(timestamped_file_name, "wb") as output_file:
        output_file.write(response.content)
        
def downloadSheet(url: str, 
                  file_path: str,
                  route: str,
                  file_ext: str=".xlsx") -> None:
    """Download Google Spreadsheet as an .xlsx file.
    """

    # Generate a timestamp string in the format YYYY-MM-DD_HH-MM-SS
    timestamp = getTimestamp()
    full_file_name = f"{timestamp}_{route}{file_ext}"
    timestamped_file_name = os.path.join(file_path, full_file_name)
    
    # SAVE GOOGLE SPREADSHEET AS .XLSX FILE
    download_url = url.replace('/edit#','/export?format=xlsx&')

    response = requests.get(download_url)

    with open(timestamped_file_name, "wb") as output_file:
        output_file.write(response.content)


# .XLSX IO
def read_excel(xlsx_path: str, **read_excel_kwargs):
    return pd.read_excel(
        xlsx_path,
        **read_excel_kwargs)

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
        references_dict (dict): Dictionary of df_name: tuple('method', 'string' , 'direction', int('col_idx1)).
            method has 2 options ['contains' and 'equals'], 'direction' has 3 options 
            ['one', 'down', 'up'] where one means only one line needs to be parsed, 'up' and 'down'
            respectively correspond to the parsing direction from the reference point.
            
            Returns:
        dict: Dictionary of {'df_name': df}
    """
    
    
    # set all cols str type, NaN -> 'nan'
    df = df.astype(str)
    
    # find reference indices
    dfs = {}
    for k,v in references_dict.items():
        
        # find ref position
        row_i, col_i = findRefRowCol(df, pattern=v[1], method=v[0])
        
        # shift ref position if specified
        col_i = v[3] if len(v) == 4 else col_i
        
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

def getNonSelectedDF(
    df_raw: pd.DataFrame, 
    df_dict: dict['df_name': pd.DataFrame], 
    start_idx: int=0, 
    stop_idx: int=None) -> pd.DataFrame:
    """Get data into DF that wasn't captured based on negative df_dict. 

    Args:
        df_raw (pd.DataFrame): Original DF where data wasn't cpatured.
        df_dict (_type_): Dict of the form {subdf_name: 'method', 'string' , 'direction', int('col_idx1))}.
        start_idx (int, optional): Starting row index (not positional).
        stop_idx (int, optional): Ending row index (not positional).

    Returns:
        pd.DataFrame: DF with rest of the info captured and NaN rows/cols stripped.
    """
    
    
    # find indicies already capture by "getDFs" function
    indices = np.array([])
    for df_ in df_dict.values():
        indices = np.concatenate((indices, df_.index.values))
    indices = [int(i) for i in indices]
    
    # subset DF
    df_sub = (df_raw
        .loc[~df_stocks_raw.index.isin(indices),:]
        .loc[start_idx:stop_idx,]
        .dropna(axis='columns', how='all')
        .dropna(axis='rows', how='all')
    )
    
    return df_sub



### DF MODIFICATION ###
def total_assets(df: pd.DataFrame, index:str, col:str) -> pd.DataFrame:
    """Calculate total value if '#ERROR!'
    """
 
    # check if total value has ERROR msg
    if df.loc[index, col] in ["#ERROR!", "#NAME?"]:
        df.loc[index, col] = 0
    else:
        return df.loc[index, col]
     
    # exclude error fields and monthly income
    df = df[(~df[col].isin(['#ERROR!', '#NAME?'])) & (df.index != 'Monthly Income')]
    
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
        'style="--bs-btn-font-size: .85rem;">Details</button>'

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

def formatToDollars(series):
    return f"${float(series):,.2f}" if isinstance(series, str) \
        and series not in ["", np.nan] \
            and all(c.isdigit() or c in ['.', '-'] \
                for c in series) else series

# Adds colors column dynamically based on risk assessment
def riskPallette(series: pd.Series, scale: dict) -> pd.Series:
    """Apply color based on risk level (# between 0-100).

    Args:
        scale (dict): Dictionary of the form {0:color, ... , 9:color}

    Returns:
        pd.Series: color
    """
    if series >= 90: 
        return scale["9"]
    if series < 10: 
        return scale["0"]
    else: 
        return scale[str(series)[0]]
    
### DF STYLING ###
def set_bg_color(val, cmap: dict) -> str:
    """Map colors to DF values based on mapping dictionary.

    Args:
        val ( any type): Any value type.
        cmap (dict): Dict of the form {val:'color'}
    """
    return f'background-color: {cmap[val]}'

def styleDf(df: pd.DataFrame, route: str):
    """Style DF using colors in .xlsx file.

    Args:
        df (pd.DataFrame): Must contain original row indices.
        route (str): Name of the route in cache folder, e.g. 'stocks_watchlist'

    """
    ## ORIGINAL DF ## 
    i1, i2 = df.columns.name if not None else df.index[0]-1, df.index[-1] + 1
    
    ## EXCEL TABLE ##
    path_to_file = f'dashboard/cache/{route}/'
    newest_file = getNewestFilename(os.listdir(path_to_file))
    full_path = path_to_file + newest_file
    
    # load workbook
    wb = openpyxl.load_workbook(filename=full_path, data_only=True)
    ws = wb.active

    # define the range of cells to read, use original df references
    rows = ws.iter_rows(max_row=i2)

    # create an empty list to hold the cell values
    row_values = []

    # iterate over the rows and columns to capture each cell properties
    for row in rows:
        cell_values = []
        for cell in row:
            # get the cell value, color, and fill
            cell_value = "" if cell.data_type in ['f'] or cell.value is None else cell.value
            cell_color = cell.fill.start_color.index if cell.fill.start_color else np.nan
            cell_fill = cell.fill.fill_type if cell.fill else np.nan

            # append the cell value, color, and fill to the list
            cell_values.append({'value': cell_value, 
                                'color': f"#{cell_color[2:]}" if isinstance(cell_color, str) else np.nan, 
                                'fill': cell_fill})

        row_values.append(cell_values)
    
    # create a pandas dataframe from the list of cell values
    df_style_dict = pd.DataFrame(row_values)
    
    new_idx = np.insert(df.index.values, 0, i1)
    df_style_dict = df_style_dict.loc[new_idx,] # get original rows
    
    df_style_dict_cols = df_style_dict.iloc[0,].apply(lambda x: x['value']) # get all cols
    df_style_dict = df_style_dict.iloc[1:,]
    df_style_dict.columns = df_style_dict_cols
    df_style_dict = df_style_dict.loc[:, df.columns] # get original rows & cols
    
    # check if respective DFs match
    assert df.shape == df_style_dict.shape, "Provided DF and Excel Table have different shape."
    assert df.index.equals(df_style_dict.index), "Provided DF and Excel Table have different row indices."
    assert df.columns.equals(df_style_dict.columns), "Provided DF and Excel Table have different column labels."
    
    # style original DF based on Excel
    styled_df = df.fillna("").style
    for i, row in df_style_dict.iterrows():
        for c, value in row.items():
            styled_dct = {'color': '#FFFFFF'} if value["color"] in ['#000000', None, np.nan] \
                else {'color': f'{value["color"]}'}
            styled_df.set_properties(subset=pd.IndexSlice[i, c], **styled_dct)
    
    return styled_df

### HELPERS ###
def get_risk_pallete(pallette: dict) -> dict['int':'color']:
    """Generate risk pallete in scale 0 to 100 in steps of 10.
    Args:
        pallette (dict): Dictionary {n: ['colors'....]}
    Returns:
        Dict: Dictionary {"0": 'color'}
    """
    return {str(i):color for i,color in enumerate(pallette(10)[::-1])}

def getTimestamp(format: str="%Y-%m-%d_%H:%M:%S") -> str:
    """Generate a timestamp string in the format YYYY-MM-DD_HH:MM:SS""" 
    return datetime.datetime.now().strftime(format)

def getOldestFilename(files: list[str], ts_format:str="%Y-%m-%d_%H:%M:%S") -> str:
    """Returns the filename with oldest timestamp"""
    ts_pattern = r"\d[\d\-_:]+\d"
    return min(files, key=lambda x: datetime.datetime.strptime(re.search(ts_pattern, x)[0][:19], ts_format))

def getNewestFilename(files: list[str], ts_format:str="%Y-%m-%d_%H:%M:%S") -> str:
    """Returns the filename with newest timestamp"""
    ts_pattern = r"\d[\d\-_:]+\d"
    return max(files, key=lambda x: datetime.datetime.strptime(re.search(ts_pattern, x)[0][:19], ts_format))

def logError(route:str, exception:Exception) -> None:
    """Save occurred error traceback to file with timestamp."""
    
    log_path = os.path.join("dashboard", "logs", "routes", route)
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    
    files = os.listdir(log_path)
    while len(files) > 9:
        oldest_file = getOldestFilename(files=files)
        os.remove(os.path.join(log_path, oldest_file))
        
    error_name = exception.__class__.__name__
    
    with open(f'{log_path}/{getTimestamp()}_{error_name}', 'a') as f: 
        traceback.print_exc(file=f)


# DECORATORS
def ioCacheAndLog(
    route: str,
    gsheet_dict:dict=None, 
    excel_dict:dict=None):
    
    def my_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # try reading data from google sheets
            try:
                io = gsheet_dict['io']
                gsheet_kwargs = {key:val for key,val in gsheet_dict.items() if key != 'io'}
                df = read_gsheet(io, **gsheet_kwargs)
                result = func(df)
                
                # download spreadsheet to cache
                cache_path = os.path.join('dashboard', 'cache', route)
                if not os.path.exists(cache_path):
                    os.mkdir(cache_path)
                    
                # don't save more than 3 files to cache
                files = os.listdir(cache_path)
                if len(files) >= 3:
                    oldest_file = getOldestFilename(files=files)
                    os.remove(os.path.join(cache_path, oldest_file))
                
                # download google sheet as .xlsx file
                downloadSheet(spreadsheet_url=io, 
                              file_path=cache_path,
                              file_name=route)
                
                return result
            
            # read data from cache
            except Exception as e:
                # capture and save occurred error log
                logError(route=route, exception=e)
                
                # read data from the newest cached file
                io_cache_path = os.path.join('dashboard', 'cache', route)
                newest_file_name = getNewestFilename(os.listdir(io_cache_path))
                df  = read_excel(os.path.join(io_cache_path, newest_file_name), **excel_dict)
                
                result = func(df)
                return result
        return wrapper
    
    return my_decorator
