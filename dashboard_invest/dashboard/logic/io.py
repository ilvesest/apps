# 3rd party imports
import requests
from bs4 import BeautifulSoup as BS


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
    