import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 70)
from collections import defaultdict
import matplotlib.pyplot as plt
from os import listdir
import plotly.graph_objects as go 
import glob
import os
import csv
import re



res = []
dir_path = r'files'
for path in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, path)):
        res.append(path)
		
		


df = pd.DataFrame([])
for file in res:
    df = pd.concat((df,pd.read_csv('files/{}'.format(file))),axis=0)
	

df.drop_duplicates(inplace=True)

from dash import Dash, dash_table, dcc, html
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "Parametri delle case in vendita su Milano nell\' anno 2024"
server = app.server 

row1 = html.Div(
    [dbc.Row([
         html.Div("Prezzi/mq quartiere Milano: ",  style={'width': '300px'},
                    ),                       
        dcc.Dropdown(df.Zone.unique().tolist(),df.Zone.unique().tolist()[0],id='dropdown1', style={'width': '300px'},
                    ),
        ], align="center")])

row2 = html.Div(
    [dbc.Row([dcc.Graph(id='graph1', style={'width': '1500px','height':'800px'})])])
        
    
row3 = html.Div(
    [dbc.Row([
        html.Div("Compara i prezzi per quartiere (max 5): " ,  style={'width': '350px'},
                    ),                       
        dbc.Col([dcc.Dropdown(df.Zone.unique().tolist(),[df.Zone.unique().tolist()[0],df.Zone.unique().tolist()[1]],id='dropdown2', multi=True,  style={'width': '200px'},
                   )]),
        html.Div("Stato di usura: " ,  style={'width': '200px'},
                    ),  
        dbc.Col([dcc.Dropdown(df.State.unique().tolist(),df.State.unique().tolist()[0],id='dropdown3',  style={'width': '200px'},
                    )]),    
    ], align="center")])


row4 = html.Div(
    [dbc.Row([dcc.Graph(id='graph2', style={'width': '1800px','height':'600px'})])])


row5 = html.Div(
    [dbc.Row([dcc.Graph(id='graph3', style={'width': '1800px','height':'600px'})])])     


row6 = html.Div(
    [dbc.Row([dcc.Graph(id='graph4', style={'width': '1800px','height':'600px'})])])    




@app.callback(
    Output('graph1', 'figure'),
    Input('dropdown1', 'value'))
def update_figure1(drop):
    fig = go.Figure()
    for m in df[df['Zone']==drop].State.unique():
        fig.add_trace(go.Box(y=df.loc[(df['Zone']==drop)&(df['State']==m),'PrSqMtr'].values, name=m))

    fig.update_layout(
        title=dict(
            text="BoxPlot Price by Mq - Zone = {}".format(drop)
        ),
        xaxis=dict(
            title=dict(
                text="Status"
            )
        ),
        yaxis=dict(
            title=dict(
                text="PrMq"
            )
        ),
        legend=dict(
            title=dict(
                text="Legend Title"
            )
        ),
        font=dict(
            family="Courier New, monospace",
            size=14,
            color="RebeccaPurple"
        )
    )
    return fig




@app.callback(
    Output('graph2', 'figure'),
    [Input('dropdown2', 'value'), Input('dropdown3', 'value')])
def update_figure2(drop1,drop2):
    fig = go.Figure()
    if len(drop1)>5:
        drop1=drop1[:5]
        
    for m in drop1:
        fig.add_trace(go.Box(y=df.loc[(df['Zone']==m)&(df['State']==drop2),'PrSqMtr'].values, name=m))

    fig.update_layout(
        title=dict(
            text="BoxPlot Price by Mq - State = {}".format(drop2)
        ),
        xaxis=dict(
            title=dict(
                text="Zone"
            )
        ),
        yaxis=dict(
            title=dict(
                text="PrMq"
            )
        ),
        legend=dict(
            title=dict(
                text="Legend Title"
            )
        ),
        font=dict(
            family="Courier New, monospace",
            size=14,
            color="RebeccaPurple"
        )
    )
    return fig




@app.callback(
    Output('graph3', 'figure'),
    [Input('dropdown2', 'value'), Input('dropdown3', 'value')])
def update_figure3(drop1,drop2):  
    m=20
    df1 = df[(df['Zone'].isin(drop1))&(df['State']==drop2)]
    fig = go.Figure()
    for k in range(0,210,10):
        fig.add_trace(go.Box(y=df1.loc[(df1['SqMeter']>m+k)&(df1['SqMeter']<m+k+10),'PrSqMtr'].values, name='{}-{}'.format(m+k,m+k+10)))

    fig.update_layout(
        title=dict(
            text="BoxPlot Price by Mq dependent on Zone {} and State {}".format(drop1,drop2)
        ),
        xaxis=dict(
            title=dict(
                text="Mq"
            )
        ),
        yaxis=dict(
            title=dict(
                text="PrMq"
            )
        ),
        legend=dict(
            title=dict(
                text="Legend Title"
            )
        ),
        font=dict(
            family="Courier New, monospace",
            size=14,
            color="RebeccaPurple"
        )
    )
    return fig


@app.callback(
    Output('graph4', 'figure'),
    [Input('dropdown2', 'value'), Input('dropdown3', 'value')])
def update_figure4(drop1,drop2):  
    
    fig = go.Figure()
    df1 = df[(df['Zone'].isin(drop1))&(df['State']==drop2)]
    fig = go.Figure(data=[go.Histogram(x=df1.loc[df1['SqMeter']<250,'SqMeter'].values,
        xbins=dict(
            start=20,
            end=250,
            size=10
        ))])
    fig.update_layout(
        title=dict(
            text="Histogram Number of House by Mq on Zone {} and State {}".format(drop1,drop2)
        ),
        xaxis=dict(
            title=dict(
                text="Mq"
            )
        ),
        yaxis=dict(
            title=dict(
                text="N"
            )
        ),
        legend=dict(
            title=dict(
                text="Legend Title"
            )
        ),
        font=dict(
            family="Courier New, monospace",
            size=14,
            color="RebeccaPurple"
        )
    )
    return fig






app.layout = dbc.Container(children=[
    html.Br(),
    row1,
    html.Br(),
    row2,
    html.Br(),
    row3,
    html.Br(),
    row4,
    html.Br(),
    row5,
    html.Br(),
    row6,
  ]
)

    
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))
