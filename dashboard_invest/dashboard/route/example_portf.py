# native imports
import re

# local imports
from dashboard.logic.constants import getMetaDataDict
from dashboard.logic.io import ioCacheAndLog, DDF
from dashboard.logic.plots import components, pie_chart


metadata = getMetaDataDict(route_name='example_portf')

@ioCacheAndLog(url=metadata['url'], route=metadata['route_name'])
def example_portf_script(ddf:DDF) -> dict:
    
    ddf = ddf.setHeader(col_names=['Asset Class', 'percent']) # set header
    
    # chop raw cs df into dict of 'name' : {'title':, 'df':, 'extra':}
    mask_df = (ddf.v
        .astype('str')
        .apply(lambda x: x.str.startswith("IDEAL PORTFOLIO"))
    )
     
    # reference indices for separate DFs 
    ref_idxs = mask_df[mask_df['Asset Class'] == True].index
    
    df_names = ['2023', 'crash_risk', 'high_inflation', 'normal']
    
    df_dict = {}
    for i, (name, i1) in enumerate(zip(df_names, ref_idxs)):
        info_dict = {}
        i2 = None if i == len(ref_idxs)-1 else ref_idxs[i+1] - 1 
        df_ = ddf.v.loc[i1:i2,:]

        info_dict['title_1'] = re.match(r"^([^\(]+)\b", df_['Asset Class'].iloc[0])[0]
        info_dict['title_2'] = re.search(r"(?![^\(]+).+", df_['Asset Class'].iloc[0])[0]
        df_clean = df_.dropna()
        df_clean['Percentage'] = df_clean['percent'].apply(lambda x: f"{int(x*100)}%")
        info_dict['df'] = df_clean
        info_dict['extra'] = df_.loc[df_clean.index[-1]+1:,:].dropna(how='all')['Asset Class']
        
        df_dict[name] = info_dict
    
    df_dict['2023']['extra'].iloc[0] += ' ' + df_dict['2023']['extra'].iloc[1]

    # prepare the DFs
    dfs = df_dict.copy()
    
    for dct in dfs.values():
        dct['df_plot'] = dct['df'].iloc[:-1,] # strip total
        dct['df_plot']['percent_n'] = (dct['df_plot']['percent'] * 100).astype(int) 
        dct['df_plot']['asset_hover'] = dct['df_plot']['Asset Class'].apply(lambda x: re.match(r"^([^\(:]+)", x)[0] if len(x)>35 else x)
        dct['df'] = dct['df'][['Asset Class', 'Percentage']]
    
    # PLOT
    hover_tt = f"""
                    <div>
                        <p style="margin:0;font-weight:bold;color:grey;">@asset_hover</p>
                        <p style="padding:0;margin:0;font-weight:bold;">@percentage_hover{{0,0}}%</p>
                    </div>
                """

    for dct in dfs.values():
        p = pie_chart(
            df=dct['df_plot'],
            x='asset_hover',
            y='percent_n',
            x_hover='asset_hover',
            percentage_decimal=0,
            label_distance=3.15,
            hover_tooltip=hover_tt,
            legend_place='below',
            fig_height=720,
            radius=0.7,
            background_color='#2C2B2B',
            label_kwargs=dict(text_font_size='12pt', text_align='center', text_font_style='bold')
        )
        dct['plot_js'], dct['plot_div'] = components(p)
        
    return dfs