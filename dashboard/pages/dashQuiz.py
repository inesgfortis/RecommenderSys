import pandas as pd
import dash
from dash import html, register_page, callback, Input, Output, dcc, State
import dash_bootstrap_components as dbc
import pickle
import time
import numpy as np
from scipy.spatial.distance import pdist, squareform
import random

seed = random.randint(1, 100)

# Load movies
with open('top_movies_dict.pkl', 'rb') as file:
    top_movies_dict = pickle.load(file)

with open('./name_to_movieID.pkl', 'rb') as file:
    name_to_movieID = pickle.load(file)

# ratings = pd.read_csv('ratings.csv')

## Dash
register_page(
    __name__,
    name='Quiz',
    top_nav=True,
    path='/Quiz'
)


########################################################################################################################
# FUNCTIONS
########################################################################################################################

def randomly_select_movies(dictionary, quantity, seed=None):
    if seed is not None:
        random.seed(seed)
    selected_keys = random.sample(list(dictionary.keys()), quantity)
    selected_dictionary = {key: dictionary[key] for key in selected_keys}
    print(selected_dictionary.keys())
    return selected_dictionary

def add_movies():
    preguntas = []
    filtered_movies = randomly_select_movies(top_movies_dict, 15,seed)

    for i, (movieId, pelicula) in enumerate(filtered_movies.items()):
        if i % 5 == 0:
            fila_preguntas = []
        
        image_path = f"{movieId}.jpg"        
        pregunta = dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(html.H4(pelicula, style={"font-size": "14px"})),
                    dbc.CardBody(
                        [
                            html.Img(src=dash.get_asset_url(image_path), style={"width": "120px", "height": "150px","margin-left": "auto", "margin-right": "auto", "display": "block"}),
                            html.Div(style={"height": "15px"}),
                            dcc.Slider(
                                id="range-slider-"+str(i+1),
                                min=0,
                                max=5,
                                step=0.5,
                                value=0,
                                marks={i: str(i) for i in range(6)}
                            ),
                        ],
                    ),
                ],
                className="col",
                style={"margin-bottom": "20px"}
            )
        )
        
        fila_preguntas.append(pregunta)
        
        if (i + 1) % 5 == 0 or i == len(filtered_movies.values()) - 1:
            fila = dbc.Row(className="row", style={"margin-bottom": "20px"}, children=fila_preguntas)
            preguntas.append(fila)
    
    return preguntas


def find_most_similar_user(ratings):

    # Create a pivot table and replace NaN values with 0
    pivot_table = pd.pivot_table(ratings, values='rating', index='userId', columns='movieId')
    pivot_table = pivot_table.fillna(0)
    
    # Compute the distance between users
    distances = pdist(pivot_table.values, metric='euclidean')

    # Find the most similar user
    distance_matrix = squareform(distances)
    userId = ratings['userId'].max()
    user_index = userId-1 # Restamos 1 porque los índices en Python comienzan desde 0

    # Select the desired distances
    user_distances = distance_matrix[user_index]

    # Find the most similar user
    most_similar_user_index = np.argmin(user_distances[np.nonzero(user_distances)])
    most_similar_user = most_similar_user_index + 1
    print("El usuario más parecido al usuario "+str(userId)+" es: ", most_similar_user)

    return most_similar_user


# Funtion to save the data introduced by the new user
def add_new_user(valores_slider):       
    ratings = pd.read_csv('ratings.csv')
    userId = ratings['userId'].max()+1
    timestamp = int(time.time())
    
    # Add the slider information to the ratings dataframe
    new_ratings = pd.DataFrame.from_dict(valores_slider, orient='index', columns=['rating'])
    new_ratings.index.name = 'movieId'
    new_ratings = new_ratings.reset_index()
    new_ratings['userId'] = userId
    new_ratings['timestamp'] = timestamp

    # Reorder the columns in new_ratings to match the order of the ratings DataFrame
    new_ratings = new_ratings.reindex(columns=ratings.columns)
    
    # Concatenate the ratings DataFrame and new_ratings to add the new lines at the end
    ratings = pd.concat([ratings, new_ratings], ignore_index=True)

    # --------------------------------- #
    #           Ucomment this           #
    # --------------------------------- #   
    # # Save the updated file
    # ratings.to_csv('ratings.csv', index=False)

    # Compute distance matrix
    most_similar_user = find_most_similar_user(ratings)

    return userId, most_similar_user



########################################################################################################################
# TAB CONTENT
########################################################################################################################

def layout():
    layout = dbc.Container([
        dbc.Card(
            [
                dbc.CardHeader("Ayúdanos a conocer tus gustos", className="bg-primary text-white"),
                dbc.CardBody(
                    add_movies()
                ),
                dbc.CardFooter(
                    [
                        html.Div(id="hidden_div_for_redirect_callback_quiz"),
                        dbc.Button("Listo", id="listo-button", color="primary", className="mr-1"),
                    ]
                ),
            ],
            className="mt-4"
        ),
        html.Div(style={"height": "30px"}),
    ])
    return layout



########################################################################################################################
# CALLBACKS
########################################################################################################################

@callback(
    Output("hidden_div_for_redirect_callback_quiz", "children"),
    # Output("new-user-id-store", "data"),
    # Output('similar-user-id-store','data'),
    Input("listo-button", "n_clicks"),
    [State("range-slider-" + str(i+1), "value") for i in range(15)]
)
def save_slider_values(n_clicks, *slider_values):
    filtered_movies = randomly_select_movies(top_movies_dict, 15,seed)
    movieIds = list(filtered_movies.keys())

    if n_clicks:
        valores_slider = {movieIds[i]: value for i, value in enumerate(slider_values)}
        print(valores_slider)
        user_id, most_similar_user = add_new_user(valores_slider)
        print(user_id)
        print(most_similar_user)
        return dcc.Location(pathname=f"/Recommendations/{most_similar_user}", id="redirect-to-recs-new-user")#, user_id,most_similar_user
    
    return None, None, None

