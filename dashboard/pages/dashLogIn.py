# Importamos las librerias mínimas necesarias
import dash
from dash import html, callback
import dash_bootstrap_components as dbc
from dash import dcc

import pandas as pd
import numpy as np

# import plotly.graph_objects as go
# import plotly.express as px
# import plotly.figure_factory as ff

from dash_bootstrap_templates import ThemeSwitchAIO

# from sys import path
# from os import getcwd
# import os
import pickle

# Load recommendations
with open('recommendations.pkl', 'rb') as file:
    recommendations = pickle.load(file)

# ml = MovieLens()
# movies_df = ml.movies
# movies_df = movies_df.sort_values('title').reset_index().drop(["index"],axis=1)



## Dash

# Main page
dash.register_page(__name__, path = "/", name = "Log In")

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
                            dbc.CardHeader("Log In", className="bg-primary text-white"),
                            dbc.CardBody(
                                [
                                    dbc.Input(type="text", id="username", placeholder="Username", className="mb-3"),
                                    dbc.Input(type="password", id="password", placeholder="Password", className="mb-3"),
                                    dbc.Button("Log In", id="login-button", color="primary", className="mt-3")
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

# Callback para seleccionar filtrar las películas en función del año
# @callback(
#     Output("graph-I", "figure"),  # recommendations 
#     [Input('filter-I', "value"),  # movie selection
#     Input('filter-II', "value"),  # genre selection --> selector opciones en lugar de dropdown
#     Input('filter-II', "value")]  # year filter    
# )

# Callback the genre input del callback de movies
# Añadir boton link (apply filters)


########################################################################################################################
########################################################################################################################