# local imports
from dashboard.logic.io import get_sheet_names, get_sheet_urls


# website URL
GSHEETS_URL = "https://docs.google.com/spreadsheets/d/" \
    "12-GISr1efphjtpuJLCfQzI2akNXxaJ1iabsG24ib71c/edit#gid=1755810028"

sheet_names = get_sheet_names(url=GSHEETS_URL) # [list] sheet names dynamically
sheet_urls = get_sheet_urls(url=GSHEETS_URL) # [dict] sheet name:url dynamically

# sheet data manually
nav_names = {
    "Investments": {
        "new name": "Portfolio",
        "routes": ["Portfolio", "", "home"],
        "title": "Overall Portfolio", 
        "page": "home_page", 
        "symbol_id": "bi bi-cash-coin"
    },
    "Investment Allocation Examples": {
        "new name":"Model Portfolios",
        "routes": ["Model Portfolios"],
        "title": "Example Portfolios", 
        "page": "portfolios_page", 
        "symbol_id": "bi bi-briefcase"
    },
    "2023 Forecasts & Risks":{
        "new name": "2023 Forecasts",
        "routes": ["2023 Forecasts"],
        "title": "2023 Forecasts & Risks",
        "page": "forecasts_page", 
        "symbol_id": "bi bi-cloud-sun"
    },
    "Stocks": {
        "new name": "Stocks",
        "routes": ["Stocks"], 
        "title": "Stocks",
        "page": "stocks_page", 
        "symbol_id": "bi bi-apple"
    },
    "Stocks Watchlist": {
        "new name": "Stocks Watchlist",
        "routes": ["Stocks Watchlist"],
        "title": "Stocks Watchlist",
        "page": "stockswatchlist_page", 
        "symbol_id": "bi bi-eye"
    },
    "Metals": {
        "new name": "Metals",
        "routes": ["Metals"],
        "title": "Precious Metals",
        "page": "home_page", 
        "symbol_id": "bi bi-gem"
    },
    "BizRE": {
        "new name": "Business & Real Estate",
        "routes": ["Business & Real Estate"],
        "title": "Business & Real Estate",
        "page": "home_page", 
        "symbol_id": "bi bi-houses"
    },
    "Crypto Consolidation": {
        "new name":"Crypto",
        "routes": ["Crypto"], 
        "title": "Crypto Investments",
        "page": "home_page", 
        "symbol_id": "bi bi-wallet2"
    },
    "Crypto INFO (SaleHODL Notes)": {
        "new name":"Crypto Watchlist",
        "routes": ["Crypto Watchlist"], 
        "title": "Crypto Watchlist",
        "page": "home_page", 
        "symbol_id": "bi bi-currency-bitcoin"
    },
    "Value Investing Ratios": {
        "new name": "Metrics",
        "routes": ["Metrics"], 
        "title": "Example Company Valuations",
        "page": "home_page", 
        "symbol_id": "bi bi-graph-up"
    },
    "X-Test Crypto": {
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