# local imports
from dashboard.logic.constants import getMetaDataDict
from dashboard.logic.io import ioCacheAndLog, DDF, getDFs, riskPallette, set_bg_color, get_risk_pallete
from bokeh.palettes import inferno

# 3rd part libraries
import pandas as pd


metadata = getMetaDataDict(route_name='forecasts')

@ioCacheAndLog(url=metadata['url'], route=metadata['route_name'], testing=True)
def forecasts_script(ddf:DDF) -> dict:
    
    results = {}
    
    # read in sub DDFs
    ddfs = ddf.getDdfDict({
        'forecasts' : ("contains", "Forecasts", "down"),
        'risks' : ("contains", "Risks", "down")
        }
    )
    
    # FORECASTS
    df_fore_styler = (ddfs['forecasts']
        .setHeader()
        .setStyle(keys=['color', 'font-weight'])
        .hide(axis='index')
    )
    results['df_fore_styler'] = df_fore_styler
    
    # RISKS
    pallette = inferno
    
    ddf_risks = (ddfs['risks']
        .setHeader()
    )
    df_risks = ddf_risks.v
    df_risks['numeric_risk'] = (df_risks # convert percentage
        .filter(regex=(r"[Rr]isk\s[Ll]evel.*"))
        .squeeze()
        .astype('float64')
        * 100
    )
    
    df_risks = df_risks.sort_values('numeric_risk', ascending=False, ignore_index=True)
    df_risks['color'] = df_risks.numeric_risk.apply(riskPallette, scale=get_risk_pallete(pallette))
    df_risks['css_ref'] = (df_risks
        .filter(regex=(r"[Rr]isks.*"))
        .squeeze()
        .str.extract(r"([A-Za-z0-9\s]+)")
        .squeeze()
        .str.replace('\s', '-', regex=True)
    )
    df_risks['string_risk'] = df_risks['numeric_risk'].apply(lambda x: f"{int(x)}%") # create string repr of %
    df_risks = df_risks.rename(columns={df_risks.columns[0]: "risk_name"}) # rename risks column
    results['df_risks'] = df_risks
    
    return results