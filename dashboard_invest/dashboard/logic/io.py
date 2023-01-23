# 3rd party imports
import requests
from bs4 import BeautifulSoup as BS
import pandas as pd


# website URL
GSHEETS_URL = "https://docs.google.com/spreadsheets/d/" \
    "1J4QvPR5mJDc44Z3_WzhWuVKB3QbxWWDzj1gLPA53ZZM/edit#gid=1755810028"
    

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
    
    df['Total_Value'] = (df['Total_Value']
        .replace(r"[\$,]", "", regex=True)
        .astype(float)
    )
    return df.reset_index()    