# native imports
from math import pi

# local imports
from dashboard.logic.io import GSHEETS_URL, read_gsheet, df_add_button

# 3rd party imports
import pandas as pd
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.models import ColumnDataSource
from bokeh.embed import components
from bokeh.resources import CDN


# Summary DF
df = read_gsheet(
    GSHEETS_URL, 
    header=None, 
    usecols=[0,1,2], 
    nrows=11,
    names=['Asset Class', 'Total Value', 'Comments']
).dropna(how='all')

# convert comment to a button
df.Comments[df.Comments.notna()] = df.Comments[df.Comments.notna()].apply(df_add_button)

# convert NaN-s to ""
df = df.fillna("")
df_style = df.copy()

# style df
df_style = df_style.style \
    .set_properties(
        subset=pd.IndexSlice[df.query("`Asset Class` == 'Total (USD)'").index, :], 
        **{"color": "#E2B842"}) \
    .set_properties(
        subset=pd.IndexSlice[df.query("`Asset Class` == 'Monthly Income'").index, :], 
        **{"color": "grey"}) \
    .hide(axis='index')

total_investments_df = df_style


# draw the plot
df1 = df.copy()
df1 = df1.drop("Comments", axis='columns').query("`Asset Class` != 'Monthly Income' & `Total Value` != '#ERROR!'")
df1['Total Value'] = df1['Total Value'].replace(r"[\$,]", "", regex=True).astype(float)
df1['angle'] = df1["Total Value"] / df1["Total Value"].sum() * 2*pi
df1['color'] = Category20c[df1.shape[0]]
df1 = df1.rename(columns={"Total Value": "total_value"})

source = ColumnDataSource(df1)

p = figure(height=350, toolbar_location=None,
           tools="hover", tooltips="Value: @total_value", x_range=(-0.5, 1.0))

p.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='Asset Class', source=source)

p.axis.axis_label = None
p.axis.visible = False
p.grid.grid_line_color = None

plot_js, plot_div = components(p) 
cdn_js = CDN.js_files[0]
cdn_css = CDN.css_files

def bokeh_pie_chart(df, x, y, radius, info_cols=None):
    
    # calculate sector start and end angles
    df['angle'] = df[y] / df[y].sum() * 2 * np.pi
    df['cumsum_start'] = df['angle'].cumsum(axis='rows').shift(1).fillna(0)
    df['cumsum_end'] = df['angle'].cumsum(axis='rows')
    
    # calculate y percentages for hover & labels
    df['percentage_number'] = (df[y] / df[y].sum() * 100).round(1)
    df['percentage_hover'] = df['percentage_number'].map('{:,.1f}%'.format)
    df['percentage_label'] = df['percentage_number'].apply(lambda x: "" if x < 5 else f"{x}%")
    
    # project label text coordinates to polar coordinates
    df['label_x_pos'] = np.cos(df['angle'].cumsum() - df['angle'].div(2)) * 3 * radius/4
    df['label_y_pos'] = np.sin(df['angle'].cumsum() - df['angle'].div(2)) * 3 * radius/4
    
    # reset dataframe index to start with 0
    df = df.reset_index(drop=True)
    
    main_source = ColumnDataSource(df)
    
    # init the figure/canvas for the plot
    p = figure(height=350, title="Asset Allocations", toolbar_location=None,
           x_range=(-1, 1.0))
    
    legend_items = []
    
    for idx, color in enumerate(Category10[df.shape[0]]):
        
        source = ColumnDataSource(df.iloc[idx,:].to_frame().T)
        
        # create the glyphs on canvas
        wedge = p.wedge(x=0, y=0, radius=radius, start_angle="cumsum_start", 
                        end_angle="cumsum_end", source=source, line_color="white", line_width=3,
                        fill_color=color, hover_fill_color=color,
                        alpha=0.7, hover_alpha=1, line_alpha=0.7, hover_line_alpha=1)
        
        p.add_tools(HoverTool(renderers=[wedge],
                              tooltips=[('', '@'+x),
                                        ('', '@'+'total_value{$0,0.00} (@percentage)')]))

        legend_items.append((df[x][idx], [wedge]))
    
    # information
    p.title.text = 'Asset Allocations'
    
    # adding % labels to the chart
    labels = LabelSet(x='label_x_pos', y='label_y_pos', text='percentage_label',
                      text_font_size='10pt', text_color="black", source=main_source,
                      text_align='center', text_alpha=0.65, text_font_style='bold')
    p.add_layout(labels)
    
    # legend
    legend = Legend(items=legend_items, location='center') 
    p.add_layout(legend, place='right')
    p.legend.click_policy="hide"
    
    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None   
    show(p)
