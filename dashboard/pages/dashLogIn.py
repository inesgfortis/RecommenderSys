# Libraries
import pickle
import dash
from dash import dcc,html, register_page, callback, Input, Output, State, ctx
import dash_bootstrap_components as dbc

# Load user-password database
with open('./user_password_dict.pkl', 'rb') as file:
    user_password_dict = pickle.load(file)


## Dash Main page
register_page(
    __name__,
    name='Home',
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
                                    html.Div(id="hidden_div_for_redirect_callback"),
                                    dbc.Button("Continuar", id="login-button", color="primary", className="mt-3", style={"width": "100%"}),
                                    html.A("¿Eres nuevo? Crea tu cuenta", href="/Register", className="mt-3", style={"text-decoration": "underline"}),
                                    dcc.ConfirmDialog(id='username-error-popup', message="User does not exist. Please register.", displayed=False),
                                    dcc.ConfirmDialog(id='password-error-popup', message="Incorrect password. Please try again.", displayed=False),
                                ],
                                style={"display": "flex", "flex-direction": "column", "align-items": "center", "justify-content": "center"}
                            ),
                        ],
                        className="mb-3",
                        style={"width": "400px", "height": "450px", "margin": "auto", "text-align": "center"}
                    ),
                    width=6,
                    style={"margin": "auto", "position": "absolute", "top": "50%", "left": "50%", "transform": "translate(-50%, -50%)"}
                )
            ),
        ],
        fluid=True,
        style={
            #"padding": "4%",
            "background-image":'url("/assets/-2.jpg")',
            "background-size": "cover",
            "height": "100vh",  # Set the height of the container to 100% viewport height
            "width": "100vw"
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

def get_user_id(username):
    for user_id, user_data in user_password_dict.items():
        if user_data['user'] == username:
            return user_id
    # Return None if the username is not found
    return None  

########################################################################################################################
# CALLBACKS
########################################################################################################################

# @callback(
#     Output('username-error-popup', 'displayed'),
#     Output('password-error-popup', 'displayed'),
#     Output('username', 'value'),
#     Output('password', 'value'),
#     Output("hidden_div_for_redirect_callback", "children"),
#     [Input('login-button', 'n_clicks')],
#     [State('username', 'value'), State('password', 'value')]
# )
# def handle_login_button(n_clicks, username, password):
#     existing_usernames = [user['user'] for user in user_password_dict.values()]

#     # User does not exist
#     if n_clicks and username not in existing_usernames:
#         return True, False, '', '', None

#     # User exists but incorrect password
#     if n_clicks and username in existing_usernames and password != get_password(username):
#         return False, True, username, '', None

#     # User exists and correct password
#     if n_clicks and username in existing_usernames and password == get_password(username):
#         return False, False, username, password, dcc.Location(pathname="/Recommendations", id="redirect-to-recs")

#     return False, False, username, password, None



@callback(
    Output('username-error-popup', 'displayed'),
    Output('password-error-popup', 'displayed'),
    Output('username', 'value'),
    Output('password', 'value'),
    Output("hidden_div_for_redirect_callback", "children"),
    Output("user-id-store", "data"),  # Store the user ID here
    [Input('login-button', 'n_clicks')],
    [State('username', 'value'), State('password', 'value')]
)
def handle_login_button(n_clicks, username, password):
    existing_usernames = [user['user'] for user in user_password_dict.values()]

    # User does not exist
    if n_clicks and username not in existing_usernames:
        return True, False, '', '', None, None

    # User exists but incorrect password
    if n_clicks and username in existing_usernames and password != get_password(username):
        return False, True, username, '', None, None

    # User exists and correct password
    if n_clicks and username in existing_usernames and password == get_password(username):
        user_id = get_user_id(username)
        print(user_id)

        return False, False, username, password, dcc.Location(pathname="/Recommendations", id="redirect-to-recs"), user_id

    return False, False, username, password, None, None



########################################################################################################################
########################################################################################################################