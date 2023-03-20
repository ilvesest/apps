# local imports
from dashboard import app, cache
from dashboard.logic.plots import cdn_js
from dashboard.logic.constants import nav_names
from dashboard.route.investments import investments_script
from dashboard.route.example_portf import example_portf_script
from dashboard.route.forecasts import forecasts_script
from dashboard.route.stocks import stocks_script
from dashboard.route.stocks_watchlist import stocks_watchlist_script

# 3rd party imports
from flask import render_template, flash
import pandas as pd


# make sheet_names global variable for all templates
@app.context_processor
@cache.cached()
def inject_sheet_names():
    return {'sheet_names': nav_names,
            'cdn_js': cdn_js}

@app.route("/")
@app.route("/home")
@app.route("/Portfolio")
@cache.cached()
def home_page():
    
    investment_dict = investments_script()
    
    # flash warning message if "#ERROR! in data"
    warning_msg = investment_dict['warning_msg'].iloc[0] + "!"
    
    if (investment_dict["df_main"].isin(['#ERROR!', '#NAME?'])).sum().sum() > 0:
        flash(warning_msg, category='danger')
    
    return render_template("home.html", **investment_dict)


@app.route("/Model Portfolios")
@cache.cached()
def portfolios_page():
    dfs = example_portf_script()
    return render_template("example_portf.html",
                           dfs=dfs)

@app.route("/2023 Forecasts")
@cache.cached()
def forecasts_page():
    forecasts_dict = forecasts_script()
    return render_template("forecasts.html", **forecasts_dict)
    
@app.route("/Stocks")
@cache.cached()
def stocks_page():
    stocks_dict = stocks_script()
    return render_template("stocks.html", **stocks_dict)
    
@app.route("/Stocks Watchlist")
@cache.cached()
def stockswatchlist_page():
    stockswatchlist_dict = stocks_watchlist_script()
    return render_template("stocks_watchlist.html", **stockswatchlist_dict)


