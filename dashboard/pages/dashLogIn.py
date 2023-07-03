# Importamos las librerias mínimas necesarias
import dash
from dash import html, callback, Input, Output, State, ctx
import dash_bootstrap_components as dbc
#from dash.dependencies import Event
from dash import dcc

import pandas as pd
import numpy as np

#from dash import redirect


# import plotly.graph_objects as go
# import plotly.express as px
# import plotly.figure_factory as ff

from dash_bootstrap_templates import ThemeSwitchAIO

# from sys import path
# from os import getcwd

import pickle

# Load recommendations
with open('./recommendations.pkl', 'rb') as file:
    recommendations = pickle.load(file)

# ml = MovieLens()
# movies_df = ml.movies
# movies_df = movies_df.sort_values('title').reset_index().drop(["index"],axis=1)



## Dash

# Main page
dash.register_page(__name__, path = "/", name = "Login")

# Filtros 2 y 3 afectando al filtro 1

########################################################################################################################
# TAB CONTENT
########################################################################################################################

layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.H2('MOVIE RECOMMENDATIONS', className='text-left text-primary, mb-3'))),  # header row

        dbc.Row(
            [
                # Login Card
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Login", className="bg-primary text-white"),
                            dbc.CardBody(
                                [
                                    dbc.Input(type="text", id="username", placeholder="Username", className="mb-3"),
                                    dbc.Input(type="password", id="password", placeholder="Password", className="mb-3"),
                                    dbc.Button("Login", id="login-button", color="primary", className="mt-3"),
                                    dcc.ConfirmDialog(id='username-error-popup', message="User does not exist. Please register.", displayed=False),
                                ]
                            ),
                        ],
                        className="mb-3"
                    ),
                    width=6,
                ),

                # New User Registration Card
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("New User Registration", className="bg-success text-white"),
                            dbc.CardBody(
                                [
                                    dbc.Input(type="text", id="new-username", placeholder="Username", className="mb-3"),
                                    dbc.Input(type="password", id="new-password", placeholder="Password", className="mb-3"),
                                    dbc.Button("Register", id="register-button", color="success", className="mt-3")
                                ]
                            ),
                        ],
                        className="mb-3"
                    ),
                    width=6,
                ),
            ]
        ),
    ],
    fluid=True,
    style={
        "padding": "4%"
    }
)

########################################################################################################################
# FUNCTIONS
########################################################################################################################






########################################################################################################################
# CALLBACKS
########################################################################################################################
existing_usernames = ["user1", "user2", "user3"]

@callback(
    Output('username-error-popup', 'displayed'),
    [Input('login-button', 'n_clicks')],
    [State('username', 'value')]
)

def handle_login_button(n_clicks, username):
    if n_clicks and username not in existing_usernames:
        return True
    return False

# @callback(
#     Output('url', 'pathname'), 
#     [Input('login-button', 'n_clicks')], 
#     [State('username', 'value'),State('password', 'value')])

# def handle_login(n_clicks, username, password):
#     if n_clicks is not None and username == 'user1' and password == '123':
#         return '/Movies'
#     else:
#         return '/'

# @callback(
#     Output('url', 'pathname'),
#     [Input('login-button', 'n_clicks')],
#     [State('username', 'value'), State('password', 'value')]
# )
# def handle_login(n_clicks, username, password):
#     if n_clicks is not None and username == 'your_username' and password == 'your_password':
#         return '/movies'
#     else:
#         return '/'


# Redirect to the recommendations page
# @callback(Output('url', 'pathname'), [Event('login-button', 'click')], [State('username', 'value'), State('password', 'value')])
# def handle_login(username, password):
#     if username == 'user1' and password == '123':
#         return '/movies'
#     else:
#         return '/'

########################################################################################################################
########################################################################################################################

# def checkUser(userId):
#     if userId in recommendations.keys():
#         return True
#     else:
#         return False
