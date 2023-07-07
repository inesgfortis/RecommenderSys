# Libraries
import dash
from dash import html, register_page, callback, Input, Output, dcc, ctx, State
import dash_bootstrap_components as dbc
import pickle
import pandas as pd
import os

# Load recommendations
with open('name_to_movieId.pkl', 'rb') as file:
    name_to_movieId = pickle.load(file)

# Load recommendations
with open('recommendations.pkl', 'rb') as file:
    recommendations = pickle.load(file)

ratings = pd.read_csv('ratings.csv')

# ---------------------------------------------------- #
# PENDIENTE: leer el userId en lugar de ponerlo a puño #
# ---------------------------------------------------- #
userId = 1

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

# Function to get the movie images associated with the recommendations for a given user
def get_recommendation_images(userId):

    numbers = [item[0] for item in recommendations[userId]]
    images = []
    for number in numbers:
        image_path = f"{number}.jpg"
        image = html.Img(src=dash.get_asset_url(image_path), style={"width": "110px", "height": "140px", "margin": "10px"})
        images.append(image)
    return images


def get_user_preferences(userId, k, like=True):

    # Filter ratings for the specified userId and sort movies by rating in descending order
    user_ratings = ratings[ratings['userId'] == userId].copy()
    sorted_movies = user_ratings.sort_values(by='rating', ascending=False)
    
    # Get the top k movies with highest ratings
    if like:
        movieIds = list(sorted_movies.head(k).copy()['movieId'])
    # Get the top k movies with lowest ratings
    else:
        movieIds = list(sorted_movies.tail(k).copy()['movieId'])

    return movieIds


# def get_movie_images(numbers):
#     images = []
#     for number in numbers:
#         image_path = f"{number}.jpg"
#         image = html.Img(src=dash.get_asset_url(image_path), style={"width": "110px", "height": "140px", "margin": "10px"})
#         images.append(image)
#     return images


import os
paths_img = os.listdir("./assets")  #Aquí iría la ruta de las imágenes y en teoría devuelve una lista de los objetos dentro de la carpeta, por ejemplo: ["20.jpg","25.jpg",...]
num_images = [int(path.split(".")[0]) for path in paths_img] # Esto deberia devolver una lista de todos los números de imágenes que tienes en la carpeta [20,25,...]

def get_movie_images(numbers):
    images = []
    for number in numbers:
        if number in num_images:
            image_path = f"{number}.jpg"
        else:
            image_path = "0.jpg"
        image = html.Img(src=dash.get_asset_url(image_path), style={"width": "110px", "height": "140px", "margin": "10px"})
        images.append(image)
    
    return images



# def get_movie_images(numbers):
#     images = []
#     for number in numbers:
#         image_path = f"{number}.jpg"
#         try:
#             image = html.Img(src=dash.get_asset_url(image_path), style={"width": "110px", "height": "140px", "margin": "10px"})
#         except:
#             image_path = "0.jpg"
#             image = html.Img(src=dash.get_asset_url(image_path), style={"width": "110px", "height": "140px", "margin": "10px"})
#         images.append(image)
#     return images



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
                            "Películas que creemos que podrían gustarte",
                            className="bg-primary text-white",
                            style={"text-align": "left", "font-size": "24px"},
                        ),
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    get_recommendation_images(userId),
                                    justify="center",
                                    align="center",
                                    className="mb-3",
                                ),
                            ],
                        ),
                        dbc.CardHeader(
                            "en base a aquellas películas que has disfrutado",
                            className="bg-primary text-white",
                            style={"text-align": "left", "font-size": "24px"},
                        ),
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    #get_movie_images(get_user_preferences(userId,10)),
                                    get_movie_images([0,1,2,3,4,5,91]),
                                    justify="center",
                                    align="center",
                                    className="mb-3",
                                ),
                            ],
                        ),
                        dbc.CardHeader(
                            "y aquellas que no te han gustado tanto",
                            className="bg-primary text-white",
                            style={"text-align": "left", "font-size": "24px"},
                        ),
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    get_movie_images(get_user_preferences(userId,10,False)),
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
        html.Div(id="hidden_div_to_end_session"),
        dbc.Button("Cerrar sesión", id="logout-button", color="secondary", className="mt-3", style={"width": "10%"}),

    ],
    fluid=True,
    style={"padding": "4%"},
)


########################################################################################################################
# CALLBACKS
########################################################################################################################

@callback(
    Output("hidden_div_to_end_session", "children"),
    Input("logout-button", "n_clicks")
)
def end_session(n_clicks):
    if n_clicks:
        return dcc.Location(pathname="/", id="redirect-to-home")
    return None


########################################################################################################################
########################################################################################################################