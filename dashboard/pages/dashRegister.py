# Libraries
from dash import dcc,html, register_page, callback, Input, Output, State
import dash_bootstrap_components as dbc
import pickle

# Load user-password database
with open('./user_password_dict.pkl', 'rb') as file:
    user_password_dict = pickle.load(file)

## Dash
register_page(
    __name__,
    name='Registration',
    top_nav=True,
    path='/Register'
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
                            dbc.CardHeader("NUEVO USUARIO", className="bg-primary text-white", style={"text-align": "left", "height": "60px", "font-size": "24px", "display": "flex", "align-items": "center"}),
                            dbc.CardBody(
                                [
                                    dbc.Input(type="text", id="new-username", placeholder="Username", className="mb-3", style={"height": "50px"}),
                                    html.Div(style={"height": "10px"}),
                                    dbc.Input(type="password", id="new-password", placeholder="Password", className="mb-3", style={"height": "50px"}),
                                    html.Div(id="hidden_div_for_redirect_callback_2"),
                                    dbc.Button("Registrarse", id="register-button", color="primary", className="mt-3", style={"width": "100%"}),
                                    html.A("¿Ya tienes una cuenta? Inicia sesión", href="/", className="mt-3", style={"text-decoration": "underline"}),
                                    dcc.ConfirmDialog(id='registration-error-popup', message="Username already exists. Please choose a different username.", displayed=False),
                                ],
                                style={"display": "flex", "flex-direction": "column", "align-items": "center", "justify-content": "center"}
                            ),
                        ],
                        className="mb-3",
                        style={"width": "400px", "height": "450px", "margin": "auto", "text-align": "center", "position": "absolute", "top": "50%", "left": "50%", "transform": "translate(-50%, -50%)"}
                    ),
                    width=6,
                    style={"margin": "auto"}
                )
            ),
        ],
        fluid=True,
        style={
            "background-image": 'url("/assets/-2.jpg")',
            "background-size": "cover",
            "height": "99vh",
            "width": "99vw"
        }
    )
    return layout


########################################################################################################################
# FUNCTIONS
########################################################################################################################

def existing_username(username):
    return username in [user['user'] for user in user_password_dict.values()]


def add_new_user(username, password):
    # Create a userId for the new user
    last_id = max(user_password_dict.keys())
    new_id = last_id + 1

    # Add the new user to the dictionary
    user_password_dict[new_id] = {"user": username, "password": password}

    # Update the file
    with open('user_password_dict.pkl', 'wb') as file:
        pickle.dump(user_password_dict, file)


########################################################################################################################
# CALLBACKS
########################################################################################################################

@callback(
    Output('registration-error-popup', 'displayed'),
    Output('new-username', 'value'),
    Output('new-password', 'value'),
    Output("hidden_div_for_redirect_callback_2", "children"),
    [Input('register-button', 'n_clicks')],
    [State('new-username', 'value'), State('new-password', 'value')]
)
def handle_register_button(n_clicks, username, password):
    if n_clicks and username and password:
        if existing_username(username):
            return True, '', '',None
        else:
            # Add the new user to the database
            add_new_user(username,password)
            return False, '', '', dcc.Location(pathname="/Quiz", id="redirect-to-quiz")

    return False, username, password, None


########################################################################################################################
########################################################################################################################