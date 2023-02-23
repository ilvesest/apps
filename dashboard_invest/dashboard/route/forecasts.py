# local imports
from dashboard.logic.constants import nav_names
from dashboard.logic.io import read_gsheet, getDFs, riskPallette, set_bg_color, get_risk_pallete
from bokeh.palettes import inferno

# 3rd part libraries
import pandas as pd

FORECASTS_URL = nav_names['2023 Forecasts & Risks']['url']

# read spreadsheet in as DF
df_fore_raw = read_gsheet(url=FORECASTS_URL, header=None)

# extract data into sub DF-s
references_dict = {
    'forecasts' : ("contains", "Forecasts", "down"),
    'risks' : ("equals", "Risks", "down")
}
df_dict_fore = getDFs(df_fore_raw, references_dict)

# FORECASTS
df_fore = df_dict_fore['forecasts'].copy()
df_fore.columns = df_fore.iloc[0]
df_fore = df_fore.iloc[1:].reset_index(drop=True)

# RISKS
df_risks = df_dict_fore['risks'].copy()
df_risks.columns = df_risks.iloc[0]
df_risks = df_risks.iloc[1:].reset_index(drop=True)
df_risks['numeric_risk'] = (df_risks
    .filter(regex=(r"[Rr]isk\s[Ll]evel.*"))
    .squeeze()
    .str.extract(r"(\d+)")
    .astype('float64')
)
df_risks = df_risks.sort_values('numeric_risk', ascending=False, ignore_index=True)
df_risks['color'] = df_risks.numeric_risk.apply(riskPallette, scale=get_risk_pallete(inferno))
df_risks['css_ref'] = (
  df_risks['Risks']
  .str.extract(r"([A-Za-z0-9\s]+)")
  .squeeze()
  .str.replace('\s', '-', regex=True)
)
df_fore_risks = df_risks


# styling
# cmap = {i:c for i,c in zip(df_risks['Risk Level in 2023'], df_risks['color'])}
# df_risks = df_risks.iloc[:,:2]
# df_fore_risks = (df_risks.style
#     .applymap(set_bg_color, cmap=cmap, subset=['Risk Level in 2023'])
#     .set_properties(subset=pd.IndexSlice[4,'Risk Level in 2023'], **{"border-bottom-right-radius": "var(--table-border-radius);"})
#     .hide(axis='index')
# )
