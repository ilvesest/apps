# 3rd part imports
import pandas as pd
import numpy as np

# bokeh
from bokeh.palettes import Category10
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Legend, LabelSet, LegendItem, HoverTool
from bokeh.embed import components
from bokeh.resources import CDN

# resoruce files to embed static bokeh to web
cdn_js = CDN.js_files[0]
cdn_css = CDN.css_files

def pie_chart(
    df: pd.DataFrame, 
    x: str, 
    y: str,
    x_hover: str=None,
    y_hover: str=None, 
    radius: float=0.8,
    x_range: tuple[float, float]=(-1, 1.0),
    percentage_decimal: int=1,
    label_distance: float=3,
    fig_height: int=350,
    background_color: str='#212529',
    pallette: dict=Category10,
    sizing_mode='scale_both',
    hover_tooltip: str='default',
    legend_place: str='right',
    fig_kwargs: dict={},
    wedge_kwargs: dict=dict(line_width=1.5, alpha=0.7),
    legend_kwargs: dict=dict(location='center', click_policy="hide",
                             label_text_color='white', border_line_width=0,
                             inactive_fill_color='#9fcf2e', inactive_fill_alpha=0.15),
    label_kwargs: dict=dict(text_font_size='10pt', text_align='center')
    ):
    
    
    # sort df by "y"
    df = df.sort_values(by=y, ignore_index=True)
    
    # calculate sector start and end angles
    df['angle'] = df[y] / df[y].sum() * 2 * np.pi
    df['cumsum_start'] = df['angle'].cumsum(axis='rows').shift(1).fillna(0)
    df['cumsum_end'] = df['angle'].cumsum(axis='rows')
    
    # calculate y percentages for hover & labels
    df['percentage_number'] = (df[y] / df[y].sum() * 100).round(percentage_decimal)
    df['percentage_hover'] = df['percentage_number'].astype(str)
    df['percentage_label'] = df['percentage_number'].apply(lambda x: "" if x < 5 else f"{x:.{percentage_decimal}f}%")
    
    # project label text coordinates to polar coordinates
    df['label_x_pos'] = np.cos(df['angle'].cumsum() - df['angle'].div(2)) * label_distance * radius/4
    df['label_y_pos'] = np.sin(df['angle'].cumsum() - df['angle'].div(2)) * label_distance * radius/4
    
    # remove assets that are 0
    df = df[df[y] > 0]
    
    # reset dataframe index to start with 0
    df = df.reset_index(drop=True)
    
    # init the figure/canvas for the plot
    p = figure(height=fig_height, 
               toolbar_location=None, 
               x_range=x_range,
               y_range=(-1.0, 1.0),
               sizing_mode=sizing_mode,
               **fig_kwargs)
    
    legend_items = []
    for idx, color in enumerate(pallette[df.shape[0]]):
        
        source = ColumnDataSource(df.iloc[idx,:].to_frame().T)
        
        # create the glyphs renderers
        wedge = p.wedge(x=0, y=0, radius=radius, start_angle="cumsum_start", 
                        end_angle="cumsum_end", source=source, **wedge_kwargs,
                        fill_color=color, hover_fill_color=color,
                        line_color=background_color, hover_line_color=background_color,
                        line_alpha=1, hover_alpha=1, hover_line_alpha=1)
        
        label = LabelSet(x='label_x_pos', y='label_y_pos', text='percentage_label',
                         source=source, level='glyph', text_color=background_color, **label_kwargs)
        
        x_hover = x if x_hover is None else x_hover
        y_hover = y if y_hover is None else y_hover
        
        hover_tooltip = hover_tooltip if hover_tooltip != 'default' else \
            f"""
                <div>
                    <p style="margin:0;font-weight:bold;color:grey;text-align:left;">@{x_hover}</p>
                    <p style="padding:0;margin:0;font-weight:bold;text-align:left;">$@{y_hover}{{0,0.00}} (@percentage_hover%)</p>
                </div>
            """
        
        p.add_layout(label)
        p.add_tools(HoverTool(renderers=[wedge],
                              tooltips=hover_tooltip))

        legend_items.append(LegendItem(label=df[x][idx], renderers=[wedge]))
    
    # legend
    legend = Legend(items=legend_items, **legend_kwargs,
                    background_fill_color=background_color) 
    p.add_layout(legend, place=legend_place)
    
    # figure attributes
    p.toolbar.active_drag = None
    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    
    
    p.min_border=0
    p.outline_line_alpha=0
    p.outline_line_width=0
    p.outline_line_color = p.background_fill_color = p.border_fill_color = background_color

    return p

def donut_chart(
    df: pd.DataFrame, 
    x: str, 
    y: str,
    x_hover: str=None,
    y_hover: str=None, 
    inner_radius: float=0.4,
    outer_radius: float=0.8,
    label_distance: float=3,
    x_range: tuple[float, float]=(-1, 1.0),
    percentage_decimal: int=1,
    fig_height: int=350,
    background_color: str='#212529',
    pallette: dict=Category10,
    sizing_mode='scale_width',
    hover_tooltip: str='default',
    legend_place: str='center',
    fig_kwargs: dict={},
    wedge_kwargs: dict=dict(line_width=3, alpha=0.7),
    legend_kwargs: dict=dict(location='center', click_policy="hide",
                             label_text_color='white', border_line_width=0,
                             inactive_fill_color='#9fcf2e', inactive_fill_alpha=0.15,
                             background_fill_alpha=0),
    label_kwargs: dict=dict(text_font_size='10pt', text_align='center')
    ):
    
    
    # sort df by "y"
    df = df.sort_values(by=y, ignore_index=True)
    
    # calculate sector start and end angles
    df['angle'] = df[y] / df[y].sum() * 2 * np.pi
    df['cumsum_start'] = df['angle'].cumsum(axis='rows').shift(1).fillna(0)
    df['cumsum_end'] = df['angle'].cumsum(axis='rows')
    
    # calculate y percentages for hover & labels
    df['percentage_number'] = (df[y] / df[y].sum() * 100).round(percentage_decimal)
    df['percentage_hover'] = df['percentage_number'].astype(str)
    df['percentage_label'] = df['percentage_number'].apply(lambda x: "" if x < 5 else f"{x:.{percentage_decimal}f}%")
    
    # project label text coordinates to polar coordinates
    df['label_x_pos'] = np.cos(df['angle'].cumsum() - df['angle'].div(2)) * label_distance * outer_radius/4
    df['label_y_pos'] = np.sin(df['angle'].cumsum() - df['angle'].div(2)) * label_distance * outer_radius/4
    
    # remove assets that are 0
    df = df[df[y] > 0]
    
    # reset dataframe index to start with 0
    df = df.reset_index(drop=True)
    
    # init the figure/canvas for the plot
    p = figure(height=fig_height, 
               toolbar_location=None, 
               x_range=x_range,
               y_range=(-1.0, 1.0),
               sizing_mode=sizing_mode,
               **fig_kwargs)
    
    legend_items = []
    for idx, color in enumerate(pallette[df.shape[0]]):
        
        source = ColumnDataSource(df.iloc[idx,:].to_frame().T)
        
        # create the glyphs renderers
        wedge = p.annular_wedge(x=0, y=0, inner_radius=inner_radius, outer_radius=outer_radius, start_angle="cumsum_start", 
                        end_angle="cumsum_end", source=source, **wedge_kwargs,
                        fill_color=color, hover_fill_color=color,
                        line_color=background_color, hover_line_color=background_color,
                        line_alpha=1, hover_alpha=1, hover_line_alpha=1)
        
        
        label = LabelSet(x='label_x_pos', y='label_y_pos', text='percentage_label',
                         source=source, level='glyph', text_color=background_color, **label_kwargs)
        
        x_hover = x if x_hover is None else x_hover
        y_hover = y if y_hover is None else y_hover
        
        hover_tooltip = hover_tooltip if hover_tooltip != 'default' else \
            f"""
                <div>
                    <p style="margin:0;font-weight:bold;color:grey;">@{x_hover}</p>
                    <p style="padding:0;margin:0;font-weight:bold;">$@{y_hover}{{0,0.00}} (@percentage_hover%)</p>
                </div>
            """
        
        p.add_layout(label)
        p.add_tools(HoverTool(renderers=[wedge],
                              tooltips=hover_tooltip))

        legend_items.append(LegendItem(label=df[x][idx], renderers=[wedge]))

    # legend
    legend = Legend(items=legend_items,  **legend_kwargs)
    
    p.add_layout(legend, place=legend_place)

    
    # figure attributes
    p.toolbar.active_drag = None
    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    
    
    p.min_border=0
    p.outline_line_alpha=0
    p.outline_line_width=0
    p.outline_line_color = p.background_fill_color = p.border_fill_color = background_color

    return p