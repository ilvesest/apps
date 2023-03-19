# local imports
from dashboard import app
from dashboard.logic.plots import cdn_js
from dashboard.logic.constants import nav_names
from dashboard.route.investments import investments_script
from dashboard.route.example_portf import example_portf_script
# from dashboard.route.stocks_watchlist import stockswatchlistScript
# from dashboard.route.forecasts import forecastsScript
# from dashboard.route.stocks import stocksScript

# 3rd party imports
from flask import render_template, flash
import pandas as pd


# make sheet_names global variable for all templates
@app.context_processor
def inject_sheet_names():
    return {'sheet_names': nav_names,
            'cdn_js': cdn_js}

@app.route("/")
@app.route("/home")
@app.route("/Portfolio")
def home_page():
    
    investment_dict = investments_script()
    
    # flash warning message if "#ERROR! in data"
    warning_msg = investment_dict['warning_msg'].iloc[0] + "!"
    
    if (investment_dict["df_main"].isin(['#ERROR!', '#NAME?'])).sum().sum() > 0:
        flash(warning_msg, category='danger')
    
    return render_template("home.html", **investment_dict)


@app.route("/Model Portfolios")
def portfolios_page():
    pass
    dfs = example_portf_script()
    return render_template("example_portf.html",
                           dfs=dfs)

@app.route("/2023 Forecasts")
def forecasts_page():
    pass
    forecasts_dict = forecastsScript()
    return render_template("forecasts.html", **forecasts_dict)
    
@app.route("/Stocks")
def stocks_page():
    pass
    stocks_dict = stocksScript()
    return render_template("stocks.html", **stocks_dict)
    
@app.route("/Stocks Watchlist")
def stockswatchlist_page():
    pass
    stockswatchlist_dict = stockswatchlistScript()
    return render_template("stocks_watchlist.html", **stockswatchlist_dict)


