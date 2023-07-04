# Importamos las librerias mínimas necesarias
import dash
from dash import html, register_page
import dash_bootstrap_components as dbc

from dash import dcc

import pickle

# # Load recommendations
# with open('recommendations.pkl', 'rb') as file:
#     recommendations = pickle.load(file)

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
register_page(
    __name__,
    name='Recommendations',
    top_nav=True,
    path='/Recommendations'
)


########################################################################################################################
# TAB CONTENT
########################################################################################################################

layout = dbc.Container(
    [
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