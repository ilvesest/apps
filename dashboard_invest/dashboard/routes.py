# local imports
from dashboard import app

from dashboard.logic.constants import nav_names
from dashboard.route.investments import investmentsScript
from dashboard.route.example_portf import dfs
from dashboard.route.stocks_watchlist import df_style, df_disc
from dashboard.route.forecasts import df_fore, df_fore_risks
from dashboard.route.stocks import df_stocks, df_stocks_info, stocks_ana_title, \
    df_stocks_ana, stock_sectors_title, df_sectors, stocks_plot_js, stocks_plot_div
from dashboard.logic.plots import cdn_js

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
    
    result_dict = investmentsScript()
    
    # flash warning message if "#ERROR! in data"
    warning_msg = result_dict['warning_msg'].iloc[0] + "!"
    
    if (result_dict["df_table"] == '#ERROR!').sum().sum() > 0:
        flash(warning_msg, category='danger')
    
    return render_template("home.html",
                           df_ads = result_dict["df_ads"], 
                           table=result_dict["styler_main"],
                           plot_js=result_dict["plot_js"], 
                           plot_div=result_dict["plot_div"],
                           df_a=result_dict["df_a"],
                           df_hist=result_dict["df_hist"],
                           df_advice=result_dict["df_advice"],
                           df_gen=result_dict["df_gen"],
                           df_risk=result_dict["df_risk"])


@app.route("/Model Portfolios")
def portfolios_page():
    return render_template("example_portf.html",
                           dfs=dfs)

@app.route("/2023 Forecasts")
def forecasts_page():
    return render_template("forecasts.html",
                           df_fore=df_fore,
                           df_fore_risks=df_fore_risks)
    
@app.route("/Stocks")
def stocks_page():
    return render_template("stocks.html",
                           df_stocks=df_stocks, 
                           df_stocks_info=df_stocks_info,
                           stocks_ana_title=stocks_ana_title, 
                           df_stocks_ana=df_stocks_ana,
                           stock_sectors_title=stock_sectors_title, 
                           df_sectors=df_sectors,
                           stocks_plot_js=stocks_plot_js,
                           stocks_plot_div=stocks_plot_div)
    
@app.route("/Stocks Watchlist")
def stockswatchlist_page():
    return render_template("stocks_watchlist.html",
                           df_style=df_style,
                           df_disc=df_disc)


