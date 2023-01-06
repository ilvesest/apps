# local imports
from dashboard import app
from dashboard.logic.io import GSHEETS_URL, get_sheet_names

# 3rd party imports
from flask import render_template

# sheet names dynamically
sheet_names = get_sheet_names(url=GSHEETS_URL)

# sheet name smanually
nav_names = {
    "Investments": "Investments",
    "Investment Allocation Examples": "Example Portfolios",
    "Stocks Watchlist": "Watchlist",
    "Metals": "Metals",
    "BizRE": "BizRE",
    "Stocks": "Stocks",
    "Value Investing Ratios": "Valuation Metrics",
    "Crypto Consolidation": "Crypto Investments",
    "Crypto INFO (SaleHODL Notes)": "Crypto INFO" 
}


# make sheet_names global variable for all templates
@app.context_processor
def inject_sheet_names():
    return {'sheet_names': nav_names}


@app.route("/")
@app.route("/home")
@app.route("/Investments")
def home_page():
    return render_template("home.html")


@app.route("/Example Portfolios")
def examples_page():
    return render_template("example_portf.html")
