# local imports
from dashboard import app

from dashboard.logic.constants import nav_names
from dashboard.route.investments import df_dict, df_ads, df_table, styler_main, \
    plot_js, plot_div, cdn_js, df_a, df_hist, df_advice, df_gen, df_risk
from dashboard.route.example_portf import dfs
from dashboard.route.stocks_watchlist import df_style, df_disc
from dashboard.route.forecasts import df_fore, df_fore_risks


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
    return render_template("forecasts.html",
                           df_fore=df_fore,
                           df_fore_risks=df_fore_risks)
    
@app.route("/Stocks Watchlist")
def stockswatchlist_page():
    return render_template("stocks_watchlist.html",
                           df_style=df_style,
                           df_disc=df_disc)


