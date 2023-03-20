# local imports
from dashboard.logic.constants import getMetaDataDict
from dashboard.logic.io import ioCacheAndLog, DDF

# 3rd party imports
import pandas as pd    

metadata = getMetaDataDict(route_name='stocks_watchlist')

@ioCacheAndLog(url=metadata['url'], route=metadata['route_name'], testing=False)
def stocks_watchlist_script(ddf:DDF) -> dict:
    """Return dict of {'obj_name': object}. Object can be pd.Series, DF, styler."""
    
    results = {}
    
    # get dict of DDFs
    ddfs = ddf.getDdfDict({
        'disclaimer': ('contains', 'These Valuations', 'down'),
        'watch': ('contains', "Neil's Value", 'down', 0)
        }
    )
    
    # DISCLAIMER DF
    df_disc = ddfs['disclaimer']

    # add period end of the sentence if not so
    df_disc = DDF(df_disc).v[0].to_frame().rename(columns={0: 'info'})
    df_disc.loc[:,'info'] = [x + '.' if x[-1] != '.' else x for x in df_disc['info']]

    # add color column and set it as cat for ordering purposes
    df_disc['color'] = ['warning', 'success', 'warning', 'success', 'success', 'danger']
    df_disc['color'] = pd.Categorical(df_disc['color'],
                                      categories=['success', 'warning', 'danger'],
                                      ordered=True)

    # add icon_id column
    icon_dict = {'warning': 'exclamation-triangle-fill', 'success': 'check-lg', 'danger':'exclamation-octagon-fill'}
    df_disc['icon_id'] = df_disc['color'].map(icon_dict)
    df_disc = df_disc.sort_values('color')
    
    # add 'df_disc' to results
    results['df_disc'] = df_disc
    
    # STOCKS WATCHLIST DF
    ddf_watch = ddfs['watch']
    df_watch_styled = (ddf_watch
        .setHeader() # set header
        .addButton(keys=['color', 'font-weight'], col_names=['Notes']) # add button
        .setStyle(keys=['color', 'font-weight'], subset=pd.IndexSlice[:, :'Sector'])
        .hide(axis='index')
        .set_table_attributes('class="stockwatch"')
    )
    # add to results
    results['df_watch_styled'] = df_watch_styled
    
    return results


    
    
