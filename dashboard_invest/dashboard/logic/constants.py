# native imports
from types import NoneType 

# local imports
from dashboard.logic.io import get_sheet_names, get_sheet_urls

# 3rd party imports
import numpy as np


# website URL
GSHEETS_URL = "https://docs.google.com/spreadsheets/d/15-kxhuk4h1BdFuiSIueamEifJpjsG6Loi621KQ8hGuY/edit#gid=1755810028"

# none type exlusion list
NONE_LIKE_LIST = ["", " ", np.nan, 'nan', 'NA', None, 'none', 'None', NoneType]

sheet_names = get_sheet_names(url=GSHEETS_URL) # [list] sheet names dynamically
sheet_urls = get_sheet_urls(url=GSHEETS_URL) # [dict] sheet name:url dynamically

# sheet data manually
nav_names = {
    "Investments": {
        "route_name":"investments",
        "new name": "Portfolio",
        "routes": ["Portfolio", "", "home"],
        "title": "Overall Portfolio", 
        "page": "home_page", 
        "symbol_id": "bi bi-cash-coin"
    },
    "Investment Allocation Examples": {
        "route_name":"example_portf",
        "new name":"Model Portfolios",
        "routes": ["Model Portfolios"],
        "title": "Example Portfolios", 
        "page": "portfolios_page", 
        "symbol_id": "bi bi-briefcase"
    },
    "2023 Forecasts & Risks":{
        "route_name":"forecasts",
        "new name": "2023 Forecasts",
        "routes": ["2023 Forecasts"],
        "title": "2023 Forecasts & Risks",
        "page": "forecasts_page", 
        "symbol_id": "bi bi-cloud-sun"
    },
    "Stocks": {
        "route_name":"stocks",
        "new name": "Stocks",
        "routes": ["Stocks"], 
        "title": "Stocks",
        "page": "stocks_page", 
        "symbol_id": "bi bi-apple"
    },
    "Stocks Watchlist": {
        "route_name":"stocks_watchlist",
        "new name": "Stocks Watchlist",
        "routes": ["Stocks Watchlist"],
        "title": "Stocks Watchlist",
        "page": "stockswatchlist_page", 
        "symbol_id": "bi bi-eye"
    },
    "Metals": {
        "route_name":"",
        "new name": "Metals",
        "routes": ["Metals"],
        "title": "Precious Metals",
        "page": "home_page", 
        "symbol_id": "bi bi-gem"
    },
    "BizRE": {
        "route_name":"",
        "new name": "Business & Real Estate",
        "routes": ["Business & Real Estate"],
        "title": "Business & Real Estate",
        "page": "home_page", 
        "symbol_id": "bi bi-houses"
    },
    "Crypto Consolidation": {
        "route_name":"",
        "new name":"Crypto",
        "routes": ["Crypto"], 
        "title": "Crypto Investments",
        "page": "home_page", 
        "symbol_id": "bi bi-wallet2"
    },
    "Crypto INFO (SaleHODL Notes)": {
        "route_name":"",
        "new name":"Crypto Watchlist",
        "routes": ["Crypto Watchlist"], 
        "title": "Crypto Watchlist",
        "page": "home_page", 
        "symbol_id": "bi bi-currency-bitcoin"
    },
    "Value Investing Ratios": {
        "route_name":"",
        "new name": "Metrics",
        "routes": ["Metrics"], 
        "title": "Example Company Valuations",
        "page": "home_page", 
        "symbol_id": "bi bi-graph-up"
    },
    "X-Test Crypto": {
        "route_name":"",
        "new name": "Test Sheet",
        "routes": ["Test Sheet"], 
        "title": "Testing Sheet",
        "page": "home_page", 
        "symbol_id": "fa-solid fa-flask-vial"
    }
}

# add sheet urls to nav-names dictionary
for name, url in sheet_urls.items():
    nav_names[name]['url'] = url
    
# STYLING CONSTANTS
styling_vars = {
    'bg-color': '#2C2B2B'
}