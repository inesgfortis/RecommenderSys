# Libraries
import dash
from dash import html, callback, Output, State, dcc
import dash_bootstrap_components as dbc

## App
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.JOURNAL], title="TFG", use_pages=True)

# app = dash.Dash(
#     __name__,
#     suppress_callback_exceptions=True,
#     external_stylesheets=[dbc.themes.JOURNAL],
#     title="TFG",
#     use_pages=True,
# )


app.layout = dbc.Container(
    children = [
        html.Br(),
        html.H1("Recommender Systems",style={'fontSize': 44}),
        html.Hr(),

        # Pages Navigator
        dbc.Nav(
                children = [
                    dbc.NavLink([
                        html.Div(page["name"]),
                    ],
                    href=page["path"],
                    active="exact",
                    )
                    for page in dash.page_registry.values()
                ],
                pills = True,
        ),

        html.Div(dash.page_container),
        dcc.Store(id='user-id-store', storage_type='memory'),         # userId associated to the recommendations
        dcc.Store(id='new-user-id-store', storage_type='memory'),
        dcc.Store(id='similar-user-id-store', storage_type='memory')  # most similar user to a new user
    ], 
    fluid = True
)



########################################################################################################################
# CALLBACKS
########################################################################################################################



########################################################################################################################
########################################################################################################################

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)

########################################################################################################################
########################################################################################################################


