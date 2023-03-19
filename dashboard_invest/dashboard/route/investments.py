# local imports
from dashboard.logic.io import DDF, ioCacheAndLog, calcTotalUSD, formatToDollars, \
    getRelContainsIdx, findRefRowCol
from dashboard.logic.constants import getMetaDataDict, styling_vars
from dashboard.logic.plots import components, pie_chart

# 3rd party imports
import pandas as pd
import re

metadata = getMetaDataDict(route_name='investments')

@ioCacheAndLog(url=metadata['url'], route=metadata['route_name'])
def investments_script(ddf:DDF) -> dict:
    
    results = {}
    
    # read in sub DDFs
    ddfs = ddf.getDdfDict({
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
    )
    
    # WARNING MSG
    results['warning_msg'] = ddfs['warning_msg'].v
    
    # ADS
    ddf_ads = ddfs['ads']
    ddf_ads.setHeader(col_names=['text', 'hyperlink'])
    
    df_ads = ddf_ads.v
    df_ads['icon'] = df_ads.text.str.extract(r"\s*(\S)")
    df_ads['text'] = df_ads.text.str.extract(r"(\b.+[^\s])")

    # manually generated headers
    headers = ['My Finance Course', 'My UK Property Courses', 'Mentoring', 'Metals Globally', 
            'Metals USA', 'Crypto Security', 'Stock Platform', 'Bank Account']
    
    # dynamically generated headers
    # headers = [" ".join(string.split()[:4]) for string in df_ads['text']]
    
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
    
    results['df_ads'] = df_ads # add ADS DF to results
    
    
    # MAIN DF
    ddf_main = DDF(ddfs['main'].iloc[:,:3])
    ddf_main = (ddf_main
        .setHeader(col_names=['Asset Class', 'Total Value', 'Notes']) # set header
        .addButton(keys=['color', 'font-weight'], col_names=['Notes']) # add button
    )
    
    df_main = ddf_main.v
    df_main = calcTotalUSD(df_main, col_name='Total Value') # calc total if errors
    df_plot = df_main.copy() # set indermediet variable for pie chart later
    df_main['Total Value'] = df_main['Total Value'].apply(formatToDollars) # apply $0,00.00 format
    df_main = df_main.fillna('').replace('#NAME?', '#ERROR!') # replace values if present
    results['df_main'] = df_main
    
    
    # get styled object
    df_main_styled = (ddf_main
        .replaceValues(df_main) # replace values based on DF vals
        .replaceProperties(pd.IndexSlice[df_main.query("`Asset Class` == 'Total (USD)'").index, :], {"color": "#E2B842"})
        .replaceProperties(pd.IndexSlice[findRefRowCol(df_main, r'Monthly Income')[0], :], {"font-style": "italic", "color": "grey"})
        .replaceProperties(pd.IndexSlice[df_main.query("`Total Value` == '#ERROR!'").index, "Total Value"], {"color": "red", "opacity": "0.75"})
        .setStyle(keys=['color', 'font-weight', 'opacity', 'font-style'])
        .hide(axis='index')
    )
    
    results['df_main_styled'] = df_main_styled # add to results
    
    # PIE-CHART
    # add underscores to col names
    df_plot.columns = df_plot.columns.map(lambda x: x.replace(" ", "_"))
    
    # set 'Asset_Class' as new index
    df_plot = (df_plot
        .set_index('Asset_Class') 
        .drop(columns=['Notes'])
        .loc[:'Total (USD)'].iloc[:-1]
        .query("Total_Value != '#ERROR!'")
        .reset_index()
        .dropna()
    )
    # set Total_Value dtype to float
    df_plot['Total_Value'] = df_plot['Total_Value'].astype(float)
    
    # create plot object
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

    plot_js, plot_div = components(pie_chart_plot) # create static plot objects
    results['plot_js'] = plot_js
    results['plot_div'] = plot_div
    
    # ASSET RISKS
    ddf_risk = ddfs['risk']
    ddf_risk = ddf_risk.setHeader(col_names=['asset', 'risk', 'notes'])
    
    df_risk = ddf_risk.v
    idx1 = getRelContainsIdx(df_risk, 'RISK') # find relative index of pattern
    idx2 = getRelContainsIdx(df_risk, 'CODE') # find relative index of pattern
    df_risk = df_risk.iloc[idx1+1:idx2,] # cut df
    df_risk.iloc[-2].notes += ". " + df_risk.iloc[-1, -1]
    df_risk = df_risk.iloc[:-1].reset_index(drop=True)
    df_risk['risk'] = [1, 1, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4]
    df_risk['risk_word'] = df_risk['risk'].replace({1:'VERY LOW', 2: 'LOW', 3: 'MEDIUM', 4: 'HIGH'})
    df_risk['li_group'] = df_risk['risk'].replace({1: 'success', 2: 'info', 3: 'warning', 4: 'danger'})
    results['df_risk'] = df_risk # add to results
    
    # ANNOUNCEMENTS
    df_a = ddfs['announce'].v
    df_a = df_a[0].str.split(pat=':', n=1, expand=True)
    df_a.columns = ['date', 'text']
    no_date_idx = df_a.index[df_a['date'].str.contains(r"property for £980k", case=False)][0]
    df_a.loc[no_date_idx, 'text'] = df_a.loc[no_date_idx, 'date']
    df_a.loc[no_date_idx, 'date'] = re.search(r"[A-Z]{1}[a-z]{2}\s202\d{1}", df_a.loc[no_date_idx, 'text'])[0]
    results['df_a'] = df_a
    
    # GENERAL ADVICE
    results['df_advice'] = ddfs['advice'].v
    
    # GENERAL NOTES
    df_gen = ddfs['general_notes'].v
    df_suc = ddfs['success'].v

    df_suc.iloc[0, 1] = df_suc.iloc[0, 1] + df_suc.iloc[-1,1]
    df_gen = pd.concat([df_gen.iloc[1:], df_suc.iloc[0,:].to_frame().T]).reset_index(drop=True)
    df_gen.columns = ['field', 'info']
    results['df_gen'] = df_gen
    
    # HISTORICAL INVESTMENTS
    df_hist = ddfs['historical'].v
    results['df_hist'] = df_hist
    
    return results
 

