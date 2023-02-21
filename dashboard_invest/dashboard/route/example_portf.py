# native imports
import re

# local imports
from dashboard.logic.io import read_gsheet
from dashboard.logic.plots import components, pie_chart


EXAMPL_PORTF_URL = "https://docs.google.com/spreadsheets/d/" \
    "1J4QvPR5mJDc44Z3_WzhWuVKB3QbxWWDzj1gLPA53ZZM/edit#gid=2145734043"
    
# read raw csv
df = read_gsheet(
    url=EXAMPL_PORTF_URL,
    header=None,
    names=['asset', 'percent']
)

# chop raw cs df into dict of 'name' : {'title':, 'df':, 'extra':}
mask_df = df.apply(lambda x: x.str.startswith("IDEAL PORTFOLIO"))

# reference indices for separate DFs 
ref_idxs = mask_df[mask_df.asset == True].index

df_names = ['2023', 'crash_risk', 'high_inflation', 'normal']
df_dict = {}
for i, (name, i1) in enumerate(zip(df_names, ref_idxs)):
    i2 = None if i == len(ref_idxs)-1 else ref_idxs[i+1]
    df_ = df.iloc[i1:i2,:]
     
    info_dict = {}
    info_dict['title_1'] = re.match(r"^([^\(]+)\b", df_.asset.iloc[0])[0]
    info_dict['title_2'] = re.search(r"(?![^\(]+).+", df_.asset.iloc[0])[0]
    info_dict['df'] = df_.dropna()
    info_dict['extra'] = df_.loc[info_dict['df'].index[-1]+1:,:].dropna(how='all').asset
    df_dict[name] = info_dict
    
df_dict['2023']['extra'].iloc[0] += ' ' + df_dict['2023']['extra'].iloc[1]

# prepare the DFs
dfs = df_dict.copy()
for v in dfs.values():
    v['df_plot'] = v['df'].iloc[:-1,] # strip total
    v['df_plot']['percent_n'] = v['df_plot']['percent'].str[:-1].astype(int) # remove '%'
    v['df_plot']['asset_hover'] = v['df_plot']['asset'].apply(lambda x: re.match(r"^([^\(:]+)", x)[0] if len(x)>35 else x)
    v['df'].columns = ['Asset Class', 'Percentage']
dfs = dfs

# PLOT
hover_tt = f"""
                <div>
                    <p style="margin:0;font-weight:bold;color:grey;">@asset_hover</p>
                    <p style="padding:0;margin:0;font-weight:bold;">@percentage_hover{{0,0}}%</p>
                </div>
            """

for dict_ in dfs.values():
    p = pie_chart(
        df=dict_['df_plot'],
        x='asset_hover',
        y='percent_n',
        x_hover='asset_hover',
        percentage_decimal=0,
        label_distance=3.15,
        hover_tooltip=hover_tt,
        legend_place='below',
        fig_height=600,
        radius=0.5,
        background_color='#2C2B2B',
        label_kwargs=dict(text_font_size='12pt', text_align='center', text_font_style='bold')
    )
    dict_['plot_js'], dict_['plot_div'] = components(p)