import pandas as pd
import dash
from dash import html, register_page, callback, Input, Output, dcc, ctx, State
import dash_bootstrap_components as dbc
import pickle
import time


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

def generar_preguntas():
    preguntas = []
    
    #for i, pelicula in enumerate(top_movies_dict.values()):
    for i, (movieId, pelicula) in enumerate(top_movies_dict.items()):
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
        
        if (i + 1) % 5 == 0 or i == len(top_movies_dict.values()) - 1:
            fila = dbc.Row(className="row", style={"margin-bottom": "20px"}, children=fila_preguntas)
            preguntas.append(fila)
    
    return preguntas

# Funtion to save the data introduced by the new user
def add_new_user(valores_slider):
    # Load new users' info
    # with open('../dashboard/valores_slider.pkl', 'rb') as file:
    #     valores_slider = pickle.load(file)
        
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
    
    # Save the updated file
    ratings.to_csv('ratings.csv', index=False)



########################################################################################################################
# TAB CONTENT
########################################################################################################################

def layout():
    layout = dbc.Container([
        dbc.Card(
            [
                dbc.CardHeader("Ayúdanos a conocer tus gustos", className="bg-primary text-white"),
                dbc.CardBody(
                    generar_preguntas()
                ),
                dbc.CardFooter(
                    [
                        #dcc.Link(html.Button("Ir a la página de inicio de sesión"), href="/inicio-sesion"),
                        dcc.Link(dbc.Button("Listo", id="listo-button", color="primary", className="mr-1"), href="/Recommendations"),
                        #dbc.Button("Listo", id="listo-button", color="primary", className="mr-1"),
                        html.Div(id="output-dictionary")  # Agregar un componente para mostrar la salida del diccionario
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
    Output("output-dictionary", "children"),  # Agrega un componente de salida ficticio
    Input("listo-button", "n_clicks"),
    [State("range-slider-" + str(i+1), "value") for i in range(len(top_movies_dict.values()))]
)
def guardar_valores_sliders(n_clicks, *slider_values):
    movieIds = list(top_movies_dict.keys())
    if n_clicks:
        valores_slider = {movieIds[i]: value for i, value in enumerate(slider_values)}
        print(valores_slider)
        add_new_user(valores_slider)
        # with open('valores_slider.pkl', 'wb') as archivo:
        #     pickle.dump(valores_slider, archivo)

    return ""


# @callback(
#     Output('url', 'pathname'),
#     Input('listo-button', 'n_clicks')
# )
# def redirect_to_movies_page(n_clicks):
#     if n_clicks:
#         return '/Recommendations'



