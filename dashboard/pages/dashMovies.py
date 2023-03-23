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


## Variables
# Hay que cargar el dataset desde la clase MovieLens()
# movies_df = pd.read_csv("ml-latest-small/movies.csv")
# movies_df = movies_df.sort_values('title').reset_index().drop(["index"],axis=1)

#from .MovieLens import MovieLens --> solo si el archivo está en la misma carpeta


#sys.path.insert(1, '\\movies')
# sys.path.insert(0,"..")
# from movies.movieLens import MovieLens
# #import MovieLens

from sys import path
from os import getcwd
import os
#path.append(str(os.getcwd())+"\\movies") # Windows
# path.append("..") 
# print("Directorio: "+os.getcwd())
# os.chdir(os.getcwd()+"\\movies")
# print("Directorio2: "+os.getcwd())
#print("Directorio: "+os.getcwd()+"\\movies")
#print(..)
#path.append(os.getcwd()+"\\movies") # Windows
#print(path)
#from .movieLens import MovieLens

# NO ENTIENDO. DA PROBLEMA PERO FUNCIONA
#os.chdir(os.getcwd()+"\\movies")
path.append(os.getcwd()+"\\movies") # Windows
print("AAAA: "+os.getcwd()+"\\movies")
#print("Directorio: "+os.getcwd())
#from movies.movieLens import MovieLens
from movieLens import MovieLens
#import movieLens

# import sys
# sys.path.insert(1, os.getcwd()+"\\movies")
# import movieLens

# Insert the path of modules folder 
# import sys
# sys.path.insert(0, str(os.getcwd())+"\\movies")
  
# # Import the module0 directly since 
# # the current path is of modules.
# from movieLens

ml = MovieLens()
movies_df = ml.movies
movies_df = movies_df.sort_values('title').reset_index().drop(["index"],axis=1)


## Dash

# Main page
#dash.register_page(__name__,name = "Movies")
#logging.getLogger('werkzeug').setLevel(logging.INFO)
dash.register_page(__name__, path = "/", name = "Movies")

# Filtros 2 y 3 afectando al filtro 1

########################################################################################################################
# TAB CONTENT
########################################################################################################################

layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.H2('MOVIE RECOMMENDATIONS', className='text-left text-primary, mb-3'))),  # header row

        ## COMPONENTES INTERACTIVAS
        ThemeSwitchAIO(aio_id="theme", themes=[dbc.themes.MINTY, dbc.themes.CYBORG]),
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
                                    {"label": movie, "value": movie} for movie in list(movies_df["title"].unique())
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
                                    {"label": movie, "value": movie} for movie in list(movies_df["title"].unique())
                                    # {"label": genre, "value": genre} for genre in diccionario ml con genres
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