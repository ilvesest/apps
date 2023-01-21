# local imports
from dashboard import app
from dashboard.logic.io import GSHEETS_URL, get_sheet_names, read_gsheet
from dashboard.data.investments import total_investments_df, plot_js, plot_div, cdn_js, cdn_css

# 3rd party imports
from flask import render_template
import pandas as pd

# sheet names dynamically
sheet_names = get_sheet_names(url=GSHEETS_URL)

# sheet name smanually
nav_names = {
    "Investments": {
        "new name": "Portfolio", 
        "title": "Overall Portfolio", 
        "page": "home_page", 
        "symbol_id": "cash-coin"
    },
    "Investment Allocation Examples": {
        "new name":"Model Portfolios", 
        "title": "Example Portfolios", 
        "page": "portfolios_page", 
        "symbol_id": "briefcase"
    },
    "Stocks": {
        "new name": "Stocks", 
        "title": "Stocks",
        "page": "home_page", 
        "symbol_id": "apple"
    },
    "Stocks Watchlist": {
        "new name": "Stocks Watchlist", 
        "title": "Stocks Watchlist",
        "page": "home_page", 
        "symbol_id": "eye"
    },
    "Metals": {
        "new name": "Metals", 
        "title": "Precious Metals",
        "page": "home_page", 
        "symbol_id": "gem"
    },
    "BizRE": {
        "new name": "Business & RE", 
        "title": "Business & Real Estate",
        "page": "home_page", 
        "symbol_id": "houses"
    },
    "Crypto Consolidation": {
        "new name":"Crypto", 
        "title": "Crypto Investments",
        "page": "home_page", 
        "symbol_id": "crypto"
    },
    "Crypto INFO (SaleHODL Notes)": {
        "new name":"Crypto Watchlist", 
        "title": "Crypto Watchlist",
        "page": "home_page", 
        "symbol_id": "wallet"
    },
    "Value Investing Ratios": {
        "new name": "Valuation Metrics", 
        "title": "Example Company Valuations",
        "page": "home_page", 
        "symbol_id": "chart"
    },
    "X-Test Crypto": {
        "new name": "Test Sheet", 
        "title": "Testing Sheet",
        "page": "home_page", 
        "symbol_id": "chart"
    }
}


# make sheet_names global variable for all templates
@app.context_processor
def inject_sheet_names():
    return {'sheet_names': nav_names,
            'cdn_js': cdn_js}


@app.route("/")
@app.route("/home")
@app.route("/Portfolio")
def home_page():
    return render_template("home.html", 
                           table=total_investments_df,
                           plot_js=plot_js,
                           plot_div=plot_div)


@app.route("/Model Portfolios")
def portfolios_page():
    return render_template("example_portf.html")


