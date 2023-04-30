# -*- coding: utf-8 -*-
"""
W.Carpenter

Graphing Data with Plotly

# https://plotly.com/python/line-charts/

"""

import plotly.graph_objects as go
import plotly.io as io
io.renderers.default='browser'
import numpy as np
import pandas as pd 

#%%
# Upload most recent working version of bout data 

source = 'https://raw.githubusercontent.com/wrcarpenter/Fixed-Income-Valuation/main/Data/tsy-par-yields.csv'  
df      = pd.read_csv(source, header=0) 
df_orig = df # preserve a copy in case

df['Date'] = pd.to_datetime(df['Date'], format="%m/%d/%Y")
df = df.sort_values(by=['Date'], ascending=True)

#%%

title = 'Treasury Par Yield (1990-2023)'

# labels = ['10 ', 'Newspaper', 'Internet', 'Radio']
# colors = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']
# mode_size = [8, 8, 12, 8]
# line_size = [2, 2, 2, 2]

dates = df["Date"]

fig = go.Figure()

# add
fig.add_trace(go.Scatter(x=dates, y=df["1 Yr"], mode='lines', name="1y", line=dict(width=1), connectgaps=True))
fig.add_trace(go.Scatter(x=dates, y=df["5 Yr"], mode='lines', name="2y", line=dict(width=1), connectgaps=True))
fig.add_trace(go.Scatter(x=dates, y=df["5 Yr"], mode='lines', name="3y", line=dict(width=1), connectgaps=True))
fig.add_trace(go.Scatter(x=dates, y=df["5 Yr"], mode='lines', name="5y", line=dict(width=1), connectgaps=True))
fig.add_trace(go.Scatter(x=dates, y=df["7 Yr"], mode='lines', name="7y", line=dict(width=1), connectgaps=True)) 
fig.add_trace(go.Scatter(x=dates, y=df["10 Yr"], mode='lines', name="10y", line=dict(width=1), connectgaps=True))
fig.add_trace(go.Scatter(x=dates, y=df["20 Yr"], mode='lines', name="20y", line=dict(width=1), connectgaps=True))
fig.add_trace(go.Scatter(x=dates, y=df["20 Yr"], mode='lines', name="30y", line=dict(width=1), connectgaps=True))


fig.update_layout(
    xaxis=dict(
        showline=True,
        showgrid=True,
        showticklabels=True,
        linecolor='black',
        linewidth=0.5,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=14,
            color='black',
        ),
    ),
    yaxis=dict(
        showgrid=True,
        zeroline=False,
        showline=True,
        ticks='outside',
        linecolor='black',
        showticklabels=True,
    ),
    autosize=False,
    width = 1500,
    height = 450,
    margin=dict(
        autoexpand=False,
        l=60,
        r=30,
        t=150,
    ),
    showlegend=True,
    plot_bgcolor='white'
)

annotations = []

# Adding labels

# Title
annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                              xanchor='center', yanchor='bottom',
                              text='Treasury Par Data',
                              font=dict(family='Arial',
                                        size=18,
                                        color='black'),
                              showarrow=False))
# Source
annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                              xanchor='center', yanchor='top',
                              text='Source: PewResearch Center & ' +
                                   'Storytelling with data',
                              font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                              showarrow=False))

fig.update_layout(annotations=annotations)

fig.show()


