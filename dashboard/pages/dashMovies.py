# Importamos las librerias mínimas necesarias
import dash
from dash import html
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
# with open('recommendations.pkl', 'rb') as file:
#     recommendations = pickle.load(file)

# ml = MovieLens()
# movies_df = ml.movies
# movies_df = movies_df.sort_values('title').reset_index().drop(["index"],axis=1)

movies = [
    {
        "title": "The Shawshank Redemption",
        "year": 1994,
        "genre": "Drama"
    },
    {
        "title": "The Godfather",
        "year": 1972,
        "genre": "Crime"
    },
    {
        "title": "Pulp Fiction",
        "year": 1994,
        "genre": "Crime"
    },
    {
        "title": "Fight Club",
        "year": 1999,
        "genre": "Drama"
    },
    {
        "title": "Forrest Gump",
        "year": 1994,
        "genre": "Drama"
    }
]


## Dash
dash.register_page(__name__,name = "Movies")

# Filtros 2 y 3 afectando al filtro 1

########################################################################################################################
# TAB CONTENT
########################################################################################################################

layout = dbc.Container(
    [
        #dbc.Row(dbc.Col(html.H2('MOVIE RECOMMENDATIONS', className='text-left text-primary, mb-3'))),  # header row

        ## COMPONENTES INTERACTIVAS
        #ThemeSwitchAIO(aio_id="theme", themes=[dbc.themes.MINTY, dbc.themes.CYBORG]),
        dbc.Row(
            [
                # Movies filter
                dbc.Col(
                    [
                        dbc.Card([
                            dbc.Label("Available Movies"),
                            dcc.Dropdown(
                                id="filter-I",
                                options =[
                                    #{"label": movie, "value": movie} for movie in list(movies_df["title"].unique())
                                    {"label": movie["title"], "value": movie["title"]} for movie in movies
                                ],
                                # Default initialization:
                                # value=(movies_df["title"][0],
                            ),
                        ],
                        # Margenes dentro del elemento Card
                        style = {
                            "padding-top": "2%",
                            "padding-left": "4%",
                            "padding-right": "4%",
                            "padding-bottom": "4%",
                            },
                        ),
                    ], 
                    style = {
                        "width":"100%",
                        "height": "100%",
                        "vertical-align": "center",

                    },          
                ),
                # Genre filter
                dbc.Col(
                    [
                        dbc.Card([
                            dbc.Label("Genres"),
                            dcc.Dropdown(
                                id="filter-II",
                                options =[
                                    {"label": movie["title"], "value": movie["title"]} for movie in movies
                                ],
                                # Default initialization:
                                # value=(movies_df["title"][0],
                            ),
                        ],
                        # Margenes dentro del elemento Card
                        style = {
                            "padding-top": "2%",
                            "padding-left": "4%",
                            "padding-right": "4%",
                            "padding-bottom": "4%",
                            },
                        ),
                    ], 
                    style = {
                        "width":"100%",
                        "height": "100%",
                        "vertical-align": "center",

                    },          
                ),
                # Year filter
                dbc.Col(
                    [
                        dbc.Card([
                            dbc.Label("Year"),
                            #dcc.RangeSlider(min(movies_df['year']), max(movies_df['year']), 5,value=[min(movies_df['year']), max(movies_df['year'])], allowCross=False, id="filter-III"),
                        ],
                        # Card margins
                        style = {
                            "padding-top": "2%",
                            "padding-left": "4%",
                            "padding-right": "4%",
                            "padding-bottom": "4%",
                            },
                        )
                    ]
                ),                
            ],style = {
                        "padding-top": "2%",
                        # quitar en caso de tener dos filtros de seleccion:
                        #"width":"50.8%", 
                        "width":"100%",
                    },  
        ),
        
        ## GRÁFICAS
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="graph-I"),lg=8), 
                # Añadir avg rating a las movies?
                #dbc.Col(dcc.Graph(id="graph-II"),lg=6),
            ],style = {
                        "padding-top": "2%",
                    }, 
        
        ),
    ], 
    # Children app layout
    fluid=True, style= {
        "padding-left": "4%",
        "padding-right": "4%",
        "padding-top": "2%",
    }, 
    
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