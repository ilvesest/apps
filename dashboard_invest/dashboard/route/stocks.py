# native
import datetime

# local imports
from dashboard.logic.constants import getMetaDataDict
from dashboard.logic.io import ioCacheAndLog, DDF, addButton
from dashboard.logic.plots import donut_chart, components

# 3rd party imports
import pandas as pd


metadata = getMetaDataDict(route_name='stocks')

@ioCacheAndLog(url=metadata['url'], route=metadata['route_name'])
def stocks_script(ddf:DDF) -> dict:
    
    results = {}
    
    # read in sub DDFs
    ddfs = ddf.getDdfDict({
        'stocks' : ("equals", "Company", "down"),
        'analysis' : ("contains", "Analysis ratio", "down"),
        'sectors1' : ("contains", "S&P500 Index", "down"),
        'sectors2' : ("contains", "Don't just buy crap! ", "up", 0)
        }
    )
    
    ### STOCKS TABLE ###
    ddf_stocks = ddfs['stocks'].setHeader()
    df_stocks = ddf_stocks.v
    
    # check if df is empty and if so is there extra info
    all_nan = df_stocks.iloc[:,1:].isna().all(axis=1)
    all_nan_idx = all_nan.loc[all_nan].index

    df_stocks_info = df_stocks.loc[all_nan].dropna(axis='columns') # info
    results['df_stocks_info'] = df_stocks_info
    
    df_stocks = df_stocks.loc[~df_stocks.index.isin(all_nan_idx),] # df stocks
    results['df_stocks'] = df_stocks
    
    ### ANALYSIS RATIOS TABLE & TITLE ###
    ddf_ana = ddfs['analysis']
    df_ana = ddf_ana.v
    
    # title of the analysis section
    stocks_ana_title = df_ana.iloc[0,0]
    results['stocks_ana_title'] = stocks_ana_title
    

    # find header index
    header_idx = df_ana.apply(lambda x: x.str.contains(r"Ratio:") == True).idxmax()[0] 
    header_cols = (df_ana
        .fillna('')
        .loc[header_idx]
        .apply(lambda x: x.strftime("%b %d") if isinstance(x, datetime.datetime) else x)
    )
    ddf_ana = DDF(ddf_ana.loc[header_idx+1:]).setHeader(col_names=header_cols)
    df_ana = ddf_ana.v

    df_ana.fillna('', inplace=True)
    joined_nan_cols = df_ana.loc[:, ""].apply(lambda x: "".join(x.astype(str)), axis=1)
    
    # capture first nan column pos index
    nan_col_idx = [i for i,col in enumerate(df_ana.columns) if col == ""][0]
    
    # remove original nan columns
    ddf_ana = DDF(ddf_ana.drop([''], axis='columns'))
    ddf_ana.insert(nan_col_idx, "Notes", joined_nan_cols)
    ddf_ana['Notes'] = ddf_ana.Notes.apply(lambda x: {'value':x}) # wrap values into dict
    df_ana_styled = (ddf_ana
        .addButton(keys=['color', 'font-weight'], col_names=['Notes']) # add Details button
        .setStyle(keys=['color', 'font-weight'])
        .hide(axis='index')
    )
    
    results['df_ana_styled'] = df_ana_styled
    
    
    ### SUGGESTED SECTORS
    stock_sectors_title = "Suggested sectors for long term value"
    results['stock_sectors_title'] = stock_sectors_title
    
    ddf_sec1 = ddfs['sectors1'].setIndex(keys=0)
    ddf_sec2 = ddfs['sectors2'].setIndex(keys=0)
    
    # prepare sectors 1 table
    df_sec1 = ddf_sec1.v.apply(lambda x: x.str.strip()) # strip leading/trailing whitespaces
    tech_label_1 = df_sec1.index[df_sec1.index.str.contains(r"tech", case=False, regex=True)][0]
    df_sec1 = (df_sec1
        .apply(lambda x: x.str.strip())
        .apply(lambda x: x+'.' if x[-1] not in ['.', '!', '?', '%', '>'] else x, axis="rows")
        .fillna("")
        .apply(lambda x: " ".join(x.astype(str)).strip(), axis=1)
    )

    # prepare sectors 2 table
    df_sec2 = ddf_sec2.v
    
    # add empty index row entry to previous
    if df_sec2.index.isna()[-1]: 
        df_sec2.iloc[-2,-1] += ' ' + df_sec2.iloc[-1,-1]

    df_sec2 = df_sec2.iloc[:-1,] # remove last row
    tech_label_2 = df_sec2.index[df_sec2.index.str.contains(r"tech", case=False, regex=True)][0]
    df_sec2 = df_sec2.rename(index={tech_label_2: tech_label_1})
    df_sec2.columns = ['Percentage', 'Notes']
    
    # join and modify tables
    df_sectors = pd.concat([df_sec1, df_sec2], axis='columns')
    
    df_sectors = (df_sectors
        .drop('Percentage', axis='columns')
        .apply(lambda x: x.str.strip())
        .apply(lambda x: x+'.' if x[-1] not in ['.', '!', '?', '%', '>'] else x, axis="rows")
        .fillna("")
        .apply(lambda x: " ".join(x.astype(str)).strip(), axis=1)
    )

    df_sectors = (pd.concat([df_sectors, df_sec2['Percentage']], axis='columns')
        .rename(columns={0: 'Notes'})
        .reset_index()
        .rename(columns={0: 'Sector'})
        .fillna("")
    )

    df_sectors = addButton(df_sectors, col_names=['Notes'])
    df_sectors['Percentage'] = df_sectors['Percentage'].apply(lambda x: f"{int(x*100)}%" if x != "" else x)
    results['df_sectors'] = df_sectors # add to results
     
    # sectors plot
    df_sectors_plot = df_sectors.copy()
    df_sectors_plot['Percentage'] = pd.to_numeric(df_sectors['Percentage'] \
        .replace(r"%", "", regex=True), errors='coerce')
    
    stocks_h_tooltip = f"""
                    <div>
                        <p style="margin:0;font-weight:bold;color:grey;">@Sector</p>
                        <p style="padding:0;margin:0;font-weight:bold;text-align:center;">@percentage_hover{{0}}%</p>
                    </div>
                """

    stocks_sectors_plot = donut_chart(
        df=df_sectors_plot.iloc[1:,],
        x='Sector',
        y='Percentage',
        sizing_mode='scale_both',
        background_color='#2C2B2B',
        percentage_decimal=0,
        fig_height=90,
        label_distance=3.1,
        label_kwargs=dict(text_font_size='12pt', text_align='center', text_font_style='bold'),
        hover_tooltip=stocks_h_tooltip,
        legend_place='center',
        fig_kwargs={'width':100}
    )

    stocks_plot_js, stocks_plot_div = components(stocks_sectors_plot)
    results['stocks_plot_js'] = stocks_plot_js
    results['stocks_plot_div'] = stocks_plot_div
    
    return results