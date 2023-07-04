# Libraries
import pickle
import dash
from dash import dcc,html, register_page, callback, Input, Output, State, ctx
import dash_bootstrap_components as dbc

# Load user-password database
with open('./user_password_dict.pkl', 'rb') as file:
    user_password_dict = pickle.load(file)


## Dash
# Main page
#dash.register_page(__name__, path = "/", name = "Home")

register_page(
    __name__,
    top_nav=True,
    path='/'
)


########################################################################################################################
# TAB CONTENT
########################################################################################################################
def layout():

    layout = dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("INICIAR SESIÓN", className="bg-primary text-white", style={"text-align": "left","height": "60px","font-size": "24px","display": "flex", "align-items": "center"}),
                            dbc.CardBody(
                                [
                                    dbc.Input(type="text", id="username", placeholder="Username", className="mb-3",style={"height": "50px"}),
                                    html.Div(style={"height": "10px"}),
                                    dbc.Input(type="password", id="password", placeholder="Password", className="mb-3",style={"height": "50px"}),
                                    dbc.Button("Continuar", id="login-button", color="primary", className="mt-3", style={"width": "100%"}),
                                    #html.Div("¿Eres nuevo? Crea tu cuenta", className="mt-3"),
                                    html.A("¿Eres nuevo? Crea tu cuenta", href="/Register", className="mt-3", style={"text-decoration": "underline"}),
                                    dcc.ConfirmDialog(id='username-error-popup', message="User does not exist. Please register.", displayed=False),
                                    dcc.ConfirmDialog(id='password-error-popup', message="Incorrect password. Please try again.", displayed=False),
                                    dcc.ConfirmDialog(id='login-success-popup', message="Successful login.", displayed=False),
                                ],
                                style={"display": "flex", "flex-direction": "column", "align-items": "center", "justify-content": "center"}
                            ),
                        ],
                        className="mb-3",
                        style={"width": "400px", "height": "450px", "margin": "auto", "text-align": "center"}
                    ),
                    width=6,
                    style={"margin": "auto"}
                )
            ),
        ],
        fluid=True,
        style={
            "padding": "4%",
            "background-image": "url('path_to_your_image')",  # Reemplaza 'path_to_your_image' con la ruta real de tu imagen
            "background-size": "cover",
        }
    )
    return layout

########################################################################################################################
# FUNCTIONS
########################################################################################################################

def get_password(username):
    for user_info in user_password_dict.values():
        if user_info['user'] == username:
            return user_info['password']
    return None


########################################################################################################################
# CALLBACKS
########################################################################################################################

# Login button (continuar)
@callback(
    Output('username-error-popup', 'displayed'),
    Output('password-error-popup', 'displayed'),
    Output('login-success-popup', 'displayed'),
    Output('username', 'value'),  # Agrega esta salida para borrar el contenido del campo de entrada del nombre de usuario
    Output('password', 'value'),  # Agrega esta salida para borrar el contenido del campo de entrada de la contraseña
    [Input('login-button', 'n_clicks')],
    [State('username', 'value'), State('password', 'value')]
)
def handle_login_button(n_clicks, username, password):
    existing_usernames = [user['user'] for user in user_password_dict.values()]

    # User does not exist
    if n_clicks and username not in existing_usernames:
        return True, False, False, '', ''

    # User exists but incorrect password
    if n_clicks and username in existing_usernames and password != get_password(username):
        return False, True, False, username, ''

    # User exists and correct password
    if n_clicks and username in existing_usernames and password == get_password(username):
        return False, False, True, '', ''

    return False, False, False, username, password


########################################################################################################################
########################################################################################################################