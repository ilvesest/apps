# local imports
from dashboard.logic.io import read_gsheet, comment_button, total_assets, \
    total_value_to_num, getDFs
from dashboard.logic.constants import GSHEETS_URL, styling_vars
from dashboard.logic.plots import components, pie_chart

# 3rd party imports
import pandas as pd
import re

# Read in summary DF and drop empty rows
df = read_gsheet(
    GSHEETS_URL, 
    header=None
)

def investments_script(df:pd.DataFrame) -> dict:

    # Extract sub DF to dictionary
    references_dict = {
        'main' : ("contains", "Monthly Income", 'up'),
        'ads' : ("contains", 'My Finance Course', 'down'),
        'announce' : ("contains", "Jul 2022: I'm", 'up'),
        'advice' : ("contains", '3x Excellent', 'up'),
        'warning_msg' : ("contains", 'NOTE: Occasionally', 'one'),
        'risk' : ("equals", "RISK", 'down', 0),
        'historical' : ("equals", "My Historical Investments", "down"),
        'cash_pos' : ("contains", "CASH POSITION", 'one'),
        'general_notes' : ("equals", "GENERAL NOTES", "down"),
        'success' : ("equals", "Investment Success:", "down")
    }

    df_dict = getDFs(df, references_dict=references_dict)

    # ADS
    df_ads = df_dict['ads'].copy()
    df_ads.columns = ['text', 'hyperlink']
    df_ads['icon'] = df_ads.text.str.extract(r"\s*(\S)")
    df_ads['text'] = df_ads.text.str.extract(r"(\b.+[^\s])")

    headers = ['My Finance Course', 'My UK Property Courses', 'Mentoring', 'Metals Globally', 
            'Metals USA', 'Metals UK', 'Crypto Security', 'Stock Platform', 'Bank Account']
    icons_html_dict = {'My Finance Course' : 'bi bi-graph-up-arrow', 
                        'My UK Property Courses' : 'bi bi-house', 
                        'Mentoring' : 'fa-regular fa-handshake', 
                        'Metals Globally': 'bi bi-globe-asia-australia', 
                        'Metals USA': 'bi bi-currency-dollar', 
                        'Metals UK': 'bi bi-currency-pound', 
                        'Crypto Security': 'bi bi-currency-bitcoin', 
                        'Stock Platform': 'fa-solid fa-chart-column', 
                        'Bank Account': 'bi bi-bank'}

    df_ads['header'] = headers
    df_ads['new_icon_html'] = df_ads['header'].map(icons_html_dict)

    ## Main DF ##
    df_table = df_dict['main'].iloc[:,:3]
    df_table.columns = ['Asset Class', 'Total Value', 'Comments']
    df_table = df_table.set_index('Asset Class')

    # if '#ERROR!' in Total (USD) recalculate the sum and assign
    df_table.loc['Total (USD)', 'Total Value'] = total_assets(df_table, 'Total (USD)', 'Total Value')

    # --------------------- Dummy Data -------------------- #
    # # Checking if asset class has error
    # df_table.loc['Business Equity', ['Total Value']] = '#ERROR!'

    # convert comment to a button
    df_table.Comments[df_table.Comments.notna()] = df_table.Comments[df_table.Comments.notna()].apply(comment_button)
    df_table = df_table.reset_index().fillna("")

    df_style = df_table.copy()

    # style df for table
    df_style = df_style.style \
        .set_properties(
            subset=pd.IndexSlice[df_table.query("`Asset Class` == 'Total (USD)'").index, :], 
            **{"color": "#E2B842"}) \
        .set_properties(
            subset=pd.IndexSlice[df_table.query("`Asset Class` == 'Monthly Income'").index, :], 
            **{"color": "grey"}) \
        .set_properties(
            subset=pd.IndexSlice[df_table.query("`Total Value` == '#ERROR!'").index, "Total Value"], 
            **{"color": "red", "opacity": "0.75"}) \
        .hide(axis='index')

    # variable for the routes.py
    styler_main = df_style

    # modify df for PIE-CHART
    df_plot = df_table.copy()
    df_plot = total_value_to_num(df_plot)

    pie_chart_plot = pie_chart(
        df=df_plot,
        x='Asset_Class',
        y='Total_Value',
        background_color=styling_vars['bg-color'],
        legend_place='below',
        fig_height=720,
        label_distance=3.2,
        label_kwargs=dict(text_font_size='9pt', text_align='center', text_font_style='bold'),
        radius=0.62,
        sizing_mode='scale_width'
    )

    plot_js, plot_div = components(pie_chart_plot)

    # ASSET RISKS
    df_risk = df_dict['risk'].copy()
    df_risk = df_risk.iloc[1:-5]
    df_risk.columns = ['asset', 'risk', 'comment']
    df_risk.iloc[-2].comment += ". " + df_risk.iloc[-1, -1]
    df_risk = df_risk.iloc[:-1].reset_index(drop=True)
    df_risk['risk'] = [1, 1, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4]
    df_risk['risk_word'] = df_risk['risk'].replace({1:'VERY LOW', 2: 'LOW', 3: 'MEDIUM', 4: 'HIGH'})
    df_risk['li_group'] = df_risk['risk'].replace({1: 'success', 2: 'info', 3: 'warning', 4: 'danger'})

    # ANNOUNCEMENTS
    df_a = df_dict['announce'].copy()
    df_a = df_a.reset_index(drop=True)
    df_a = df_a[0].str.split(pat=':', n=1, expand=True)
    df_a.columns = ['date', 'text']
    no_date_idx = df_a['date'].str.contains(r"property for £980k", case=False).argmax()
    df_a.loc[no_date_idx, 'text'] = df_a.loc[no_date_idx, 'date']
    df_a.loc[no_date_idx, 'date'] = re.search(r"[A-Z]{1}[a-z]{2}\s202\d{1}", df_a.loc[no_date_idx, 'text'])[0]


    # GENERAL ADVICE
    df_advice = df_dict['advice'].copy()
    df_advice = df_advice.reset_index(drop=True)

    # GENERAL NOTES
    df_gen = df_dict['general_notes'].copy()
    df_suc = df_dict['success'].copy()

    df_suc.iloc[0, 1] = df_suc.iloc[0, 1] + df_suc.iloc[-1,1]
    df_gen = pd.concat([df_gen.iloc[1:], df_suc.iloc[0,:].to_frame().T]).reset_index(drop=True)
    df_gen.columns = ['field', 'info']

    # HISTORICAL INVESTMENTS
    df_hist = df_dict['historical'].copy()
    df_hist = df_hist.reset_index(drop=True)


def run_script()

try:
    df = 
    investments_dict = investments_script()    

