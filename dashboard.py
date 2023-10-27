import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import json
from callbacks import *

def create_dashboard(app, fig_year, fig_sx, fig_activity, fig_world, fig_hours, fig_time_periods, fig_age):
    app.layout = html.Div(style={'backgroundColor': 'cornsilk'}, children=[
        dcc.Tabs([#different tabs, each tab is for a graph
            dcc.Tab(id = 'tab1',label='Years', children=[#first graph : number of attacks according to the age
                dcc.Tab(label='tab1', children=[
                    html.Div([
                        dcc.Graph(id='graph1', figure=fig_year),#we reload the fig
                        html.Div(
                            id = 'description1', 
                            children = "the number of shark attacks by years",#description on the dashboard for this tab
                            style={'text-align': 'center', 'font-size': '22px', 'margin-top': '50px'}#description visual
                            )
                    ])
                ])
            ]),
            dcc.Tab(id= 'tab2',label='Gender', children=[
                html.Div([#first graph : number of attacks according to the gender
                    dcc.Graph(id='graph2', figure=fig_sx),#we reload the fig
                    html.Div(
                        id = 'description2',
                        children = "the proportion of shark attack by genders since 1800",#description on the dashboard for this tab
                        style={'text-align': 'center', 'font-size': '22px', 'margin-top': '50px'}#description visual
                        )
                ])
            ]),
            dcc.Tab(id= 'tab3', label='Fatal or not', children=[
                html.Div([
                    dcc.Dropdown(
                        id='fatal-dropdown', 
                        options=[#dropdown options
                            {'label' : 'fatal attack', 'value' : 'Y'},
                            {'label' : 'not fatal attack', 'value' : 'N'}
                        ],
                        value = 'Y',#value at the beginning
                        style={'width': '50%'}#size
                    ),
                    dcc.Graph(id='graph3'),
                    html.Div(
                        id = 'description3',
                        children = "the number of fatal or not attacks by known shark species since 1800",#description on the dashboard for this tab
                        style={'text-align': 'center', 'font-size': '22px', 'margin-top': '50px'}#description visual
                        )  
                ])
            ]),

            dcc.Tab(id= 'tab4', label='Activity', children=[
                html.Div([
                    dcc.Graph(id='graph4', figure=fig_activity),#we reload the fig
                    html.Div(
                        id = 'description4',
                        children = "the number of shark attack by human activity since 1800",#description on the dashboard for this tab
                        style={'text-align': 'center', 'font-size': '22px', 'margin-top': '50px'}#description visual
                        )
                ])
            ]),
            dcc.Tab(label='Shark Attack Map', children=[
            html.Div([
                html.Div(
                        id = 'text_dropdown',
                        children = "Map :",
                        style={'text-align': 'left', 'font-size': '18px', 'margin-top': '10px'}#description visual
                        ),
                dcc.Dropdown(
                    id='shark-attack-details-dropdown',
                    options=[
                        {'label': 'World', 'value': 'World'},
                        {'label': 'USA', 'value': 'usa'},
                        {'label': 'Australia', 'value': 'australia'},
                        {'label': 'South Africa', 'value': 'south-africa'},
                    ],#dropdown options
                    value='World'#value at the beginning
                ),
                dcc.Graph(id='graph_maps', figure=fig_world),#we reload the fig
            ])
        ]),
            dcc.Tab(id= 'tab5',label='Time', children=[
                html.Div([
                    dcc.Graph(id='graph5', figure=fig_hours),#we reload the fig1
                    dcc.Graph(id='graph6', figure=fig_time_periods),#we reload the fig2
                ]),
            ]),
            dcc.Tab(id= 'tab6',label='Attacks by age', children=[
                html.Div([
                    dcc.Checklist(
                        id='show-details-checkbox',
                        options=[
                            {'label': 'Show Details', 'value': 'show-details'}#chekclist options
                        ],
                        value=['show-details'],#value at the beginning
                        style={'font-size': '20px'}#size
                        ),
                    dcc.Graph(id='graph7', figure=fig_age),#we reload the fig
                    
                ]),
                
            ]),

        ])
    ])
    
    
    
    