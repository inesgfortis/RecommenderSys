# Importamos las librerias mínimas necesarias
import dash
from dash import html, register_page
import dash_bootstrap_components as dbc

from dash import dcc

import pickle
import os
from PIL import Image


# Load recommendations
with open('name_to_movieId.pkl', 'rb') as file:
    name_to_movieId = pickle.load(file)

# Load recommendations
with open('recommendations.pkl', 'rb') as file:
    recommendations = pickle.load(file)


## Dash
register_page(
    __name__,
    name='Recommendations',
    top_nav=True,
    path='/Recommendations'
)

########################################################################################################################
# FUNCTIONS
########################################################################################################################

# Function to get movie images by number
# def get_movie_images(numbers):
#     images = []
#     for number in numbers:
#         image_path = f"{number}.jpg"
#         image = html.Img(src=dash.get_asset_url(image_path), style={"width": "110px", "height": "140px", "margin": "10px"})
#         images.append(image)
#     return images

def get_movie_images(userId):

    numbers = [item[0] for item in recommendations[userId]]
    images = []
    for number in numbers:
        image_path = f"{number}.jpg"
        image = html.Img(src=dash.get_asset_url(image_path), style={"width": "110px", "height": "140px", "margin": "10px"})
        images.append(image)
    return images



########################################################################################################################
# TAB CONTENT
########################################################################################################################

layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            "Recomendaciones",
                            className="bg-primary text-white",
                            style={"text-align": "center", "font-size": "24px"},
                        ),
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    # PENDIENTE: leer el userId en lugar de ponerlo a puño
                                    get_movie_images(1),
                                    justify="center",
                                    align="center",
                                    className="mb-3",
                                ),
                            ],
                        ),
                        dbc.CardHeader(
                            "Películas que te han gustado",
                            className="bg-primary text-white",
                            style={"text-align": "center", "font-size": "24px"},
                        ),
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    get_movie_images(1),
                                    justify="center",
                                    align="center",
                                    className="mb-3",
                                ),
                            ],
                        ),
                        dbc.CardHeader(
                            "Películas valoradas negativamente",
                            className="bg-primary text-white",
                            style={"text-align": "center", "font-size": "24px"},
                        ),
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    get_movie_images(1),
                                    justify="center",
                                    align="center",
                                    className="mb-3",
                                ),
                            ],
                        ),
                    
                    ],
                    style={"width": "1400px", "margin": "auto"},
                ),
            ),
        ),
        html.Div(style={"height": "10px"}),
        dbc.Button("Cerrar sesión", id="logout-button", color="secondary", className="mt-3", style={"width": "10%"}),

    ],
    fluid=True,
    style={"padding": "4%"},
)


########################################################################################################################
# CALLBACKS
########################################################################################################################





########################################################################################################################
########################################################################################################################