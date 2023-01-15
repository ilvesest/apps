# local imports
from dashboard import app
from dashboard.logic.io import GSHEETS_URL, get_sheet_names, read_gsheet
from dashboard.data.investments import total_investments_df

# 3rd party imports
from flask import render_template
import pandas as pd

# sheet names dynamically
sheet_names = get_sheet_names(url=GSHEETS_URL)

# sheet name smanually
nav_names = {
    "Investments": {"new name": "Portfolio", "title": "Overall Portfolio"},
    "Investment Allocation Examples": {"new name":"Model Portfolios", "title": "Example Portfolios"},
    "Stocks": {"new name": "Stocks", "title": "Stocks"},
    "Stocks Watchlist": {"new name": "Stocks Watchlist", "title": "Stocks Watchlist"},
    "Metals": {"new name": "Metals", "title": "Precious Metals"},
    "BizRE": {"new name": "Business & RE", "title": "Business & Real Estate"},
    "Crypto Consolidation": {"new name":"Crypto", "title": "Ctypto Investments"},
    "Crypto INFO (SaleHODL Notes)": {"new name":"Crypto Watchlist", "title": "Crypto Watchlist"},
    "Value Investing Ratios": {"new name": "Valuation Metrics", "title": "Example Company Valuations"},
    "X-Test Crypto": {"new name": "Test Sheet", "title": "Testing Sheet"}
}


# make sheet_names global variable for all templates
@app.context_processor
def inject_sheet_names():
    return {'sheet_names': nav_names}


@app.route("/")
@app.route("/home")
@app.route("/Portfolio")
def home_page():
    return render_template("home.html", table=total_investments_df)


@app.route("/Example Portfolios")
def examples_page():
    return render_template("example_portf.html")
