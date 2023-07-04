# Importamos las librerias mínimas necesarias
import dash
from dash import dcc,html, callback, Input, Output, State, ctx
import dash_bootstrap_components as dbc
# import pandas as pd
# import numpy as np

import pickle

# # Load recommendations
# with open('./recommendations.pkl', 'rb') as file:
#     recommendations = pickle.load(file)


# Load user-password database
with open('./user_password_dict.pkl', 'rb') as file:
    user_password_dict = pickle.load(file)


## Dash
# Main page
dash.register_page(__name__, path = "/", name = "Login")


########################################################################################################################
# TAB CONTENT
########################################################################################################################

layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.H2('MOVIE RECOMMENDATIONS', className='text-left text-primary, mb-3'))),  # header row

        dbc.Row(
            [
                # Login Card
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Login", className="bg-primary text-white"),
                            dbc.CardBody(
                                [
                                    dbc.Input(type="text", id="username", placeholder="Username", className="mb-3"),
                                    dbc.Input(type="password", id="password", placeholder="Password", className="mb-3"),
                                    dbc.Button("Login", id="login-button", color="primary", className="mt-3"),
                                    dcc.ConfirmDialog(id='username-error-popup', message="User does not exist. Please register.", displayed=False),
                                    dcc.ConfirmDialog(id='password-error-popup', message="Incorrect password. Please try again.", displayed=False),
                                    dcc.ConfirmDialog(id='login-success-popup', message="Successful login.", displayed=False),
                                ]
                            ),
                        ],
                        className="mb-3"
                    ),
                    width=6,
                ),

                # New User Registration Card
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("New User Registration", className="bg-success text-white"),
                            dbc.CardBody(
                                [
                                    dbc.Input(type="text", id="new-username", placeholder="Username", className="mb-3"),
                                    dbc.Input(type="password", id="new-password", placeholder="Password", className="mb-3"),
                                    dbc.Button("Register", id="register-button", color="success", className="mt-3")
                                ]
                            ),
                        ],
                        className="mb-3"
                    ),
                    width=6,
                ),
            ]
        ),
    ],
    fluid=True,
    style={
        "padding": "4%"
    }
)


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

# Login button
@callback(
    Output('username-error-popup', 'displayed'),
    Output('password-error-popup', 'displayed'),
    Output('login-success-popup', 'displayed'),
    [Input('login-button', 'n_clicks')],
    [State('username', 'value'), State('password', 'value')]
)

def handle_login_button(n_clicks, username, password):
    existing_usernames = [user['user'] for user in user_password_dict.values()]

    # User does not exist
    if n_clicks and username not in existing_usernames:
        return True, False, False

    # User exists but incorrect password
    if n_clicks and username in existing_usernames and password != get_password(username):
        return False, True, False
    
    # User exists and correct password
    if n_clicks and username in existing_usernames and password == get_password(username):
        return False, False, True

    return False, False, False



########################################################################################################################
########################################################################################################################

# def checkUser(userId):
#     if userId in recommendations.keys():
#         return True
#     else:
#         return False
