# Libraries
import dash
from dash import html, register_page
import dash_bootstrap_components as dbc
import pickle
import pandas as pd

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


def get_movie_images(numbers):
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
                                    get_recommendation_images(userId),
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
                                    get_movie_images(get_user_preferences(userId,10)),
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