# local imports
from dashboard import app
from dashboard.logic.io import GSHEETS_URL, get_sheet_names, get_sheet_urls
from dashboard.route.investments import df_dict, df_ads, df_table, styler_main, \
    plot_js, plot_div, cdn_js, df_a, df_hist, df_advice, df_gen, df_risk
from dashboard.route.example_portf import dfs
from dashboard.route.stocks_watchlist import df_style, df_disc


# 3rd party imports
from flask import render_template, flash
import pandas as pd

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
        "page": "home_page", 
        "symbol_id": "bi bi-cloud-sun"
    },
    "Stocks": {
        "new name": "Stocks",
        "routes": ["Stocks"], 
        "title": "Stocks",
        "page": "home_page", 
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



# make sheet_names global variable for all templates
@app.context_processor
def inject_sheet_names():
    return {'sheet_names': nav_names,
            'cdn_js': cdn_js}

@app.route("/")
@app.route("/home")
@app.route("/Portfolio")
def home_page():

    # flash warning message if "#ERROR! in data"
    warning_msg = df_dict['warning_msg'].iloc[0] + "!"
    
    if (df_table == '#ERROR!').sum().sum() > 0:
        flash(warning_msg, category='danger')
    
    return render_template("home.html",
                           df_ads = df_ads, 
                           table=styler_main,
                           plot_js=plot_js, 
                           plot_div=plot_div,
                           df_a=df_a,
                           df_hist=df_hist,
                           df_advice=df_advice,
                           df_gen=df_gen,
                           df_risk=df_risk)


@app.route("/Model Portfolios")
def portfolios_page():
    return render_template("example_portf.html",
                           dfs=dfs)

@app.route("/2023 Forecasts")
def forecasts_page():
    return render_template("forecasts.html")
    
@app.route("/Stocks Watchlist")
def stockswatchlist_page():
    return render_template("stocks_watchlist.html",
                           df_style=df_style,
                           df_disc=df_disc)


