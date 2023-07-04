import pandas as pd
import dash
from dash import html, register_page, callback, Input, Output, dcc, ctx, State
import dash_bootstrap_components as dbc
import pickle


# Load movies
with open('top_movies_dict.pkl', 'rb') as file:
    top_movies_dict = pickle.load(file)

with open('./name_to_movieID.pkl', 'rb') as file:
    name_to_movieID = pickle.load(file)

ratings = pd.read_csv('ratings.csv')

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
    
    for i, pelicula in enumerate(top_movies_dict.values()):
        if i % 5 == 0:
            fila_preguntas = []
        
        pregunta = dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(html.H4(pelicula, style={"font-size": "14px"})),
                    dbc.CardBody(
                        dcc.Slider(
                            id="range-slider-"+str(i+1),
                            min=0,
                            max=5,
                            step=0.5,
                            value=0,
                            marks={i: str(i) for i in range(6)}
                        )
                    ),
                    # dbc.CardFooter(
                    #     dbc.Button("Guardar", id={"type": "guardar-button", "index": i}, color="primary", className="mr-1")
                    # )
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



########################################################################################################################
# TAB CONTENT
########################################################################################################################

def layout():
    layout = dbc.Container(
        dbc.Card(
            [
                dbc.CardHeader("Cuestionario", className="bg-primary text-white"),
                dbc.CardBody(
                    generar_preguntas()
                ),
                dbc.CardFooter(
                    dbc.Button("Listo", id="listo-button", color="primary", className="mr-1")
                ),
                dbc.CardFooter(
                    html.Div(id="output-dictionary")  # Agregar un componente para mostrar la salida del diccionario
                ),
            ],
            className="mt-4"
        )
    )
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
    if n_clicks:
        valores_slider = {i+1: value for i, value in enumerate(slider_values)}
        print("dentro")
        with open('valores_slider.pkl', 'wb') as archivo:
            pickle.dump(valores_slider, archivo)
    
    return ""




