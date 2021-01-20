#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import geoviews as gv
import geoviews.tile_sources as gvts
from geoviews import dim, opts
from bokeh.models import HoverTool
from bokeh.plotting import figure, output_file, save


#read and replace NaN state values with '-'
df_new= pd.read_csv("03-24-2020.csv")[['Province_State','Country_Region','Lat','Long_','Confirmed','Deaths','Recovered']]
df_new = df_new.fillna('-')

#rename columns
df_new.columns = ['state', 'country', 'lat', 'lon', 'confirmed', 'deaths', 'recovered']


# In[2]:

gv.extension('bokeh')

#define custom tooltip with color code
hover = HoverTool(
        tooltips="""
        <div>
            <span>State:</span>
            <span>@state</span>
        </div>
        <div>
            <span>Country:</span>
            <span>@country</span>
        </div>
        <div>
            <span>Confirmed:</span>
            <span style="background-color: red; color:white;">&nbsp;@confirmed&nbsp;</span>
        </div>
        <div>
            <span>Recovered:</span>
            <span style="background-color: springgreen;">&nbsp;@recovered&nbsp;</span>
        </div>
        <div>
            <span>Deaths:</span>
            <span style="background-color: black; color:white;">&nbsp;@deaths&nbsp;</span>
        </div>
        """
    )


confirmed_points = gv.Points(df_new, ['lon', 'lat'], ['state', 'country', 'confirmed', 'deaths', 'recovered'])
recovered_points = gv.Points(df_new, ['lon', 'lat'], ['state', 'country', 'confirmed', 'deaths', 'recovered'])
death_points = gv.Points(df_new, ['lon', 'lat'], ['state', 'country', 'confirmed', 'deaths', 'recovered'])

#options for data points 
confirmed_opts = opts.Points(width=1200, height=700, alpha=0.4, hover_line_color='red',  
                line_color='red', color='red', xaxis=None, yaxis=None,
                tools=[hover],size=np.sqrt(dim('confirmed'))*0.7, hover_fill_alpha=0.6)

recovered_opts = opts.Points(width=1200, height=700, alpha=0.6, hover_line_color='green',  
                line_color='springgreen', color='springgreen', xaxis=None, yaxis=None,
                tools=[hover],size=np.sqrt(dim('recovered'))*0.7, hover_fill_alpha=0.8)

death_opts = opts.Points(width=1200, height=700, alpha=0.7, hover_line_color='black',  
                line_color='black', color='black', xaxis=None, yaxis=None,
                tools=[hover],size=np.sqrt(dim('deaths'))*0.7, hover_fill_alpha=0.9)

#overlay of data points on tile source
p = gvts.CartoDark * confirmed_points.opts(confirmed_opts)* recovered_points.opts(recovered_opts)* death_points.opts(death_opts)

renderer = gv.renderer('bokeh')

renderer.save(p, 'dashboard')

#output_file('plot.html', title='Bokeh Plot', autosave=False, mode='inline', root_dir=None)
