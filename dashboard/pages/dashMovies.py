# Importamos las librerias mínimas necesarias
import dash
from dash import html, register_page
import dash_bootstrap_components as dbc

from dash import dcc

import pickle
import os



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
def get_movie_images(numbers):
    image_folder = "images/"
    images = []
    for number in numbers:
        image_path = os.path.join(image_folder, f"{number}.jpg")
        #print(image_path)
        if os.path.isfile(image_path):
            print("dentro")
            image = html.Img(src=image_path, style={"width": "110px", "height": "140px", "margin": "10px"})
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
                                    get_movie_images([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
                                    justify="center",
                                    align="center",
                                    className="mb-3",
                                ),
                            ],
                        ),
                    
                    ],
                    style={"width": "1400px", "margin": "auto"},
                )
            )
        ),
    ],
    fluid=True,
    style={"padding": "4%"},
)


########################################################################################################################
# CALLBACKS
########################################################################################################################





########################################################################################################################
########################################################################################################################