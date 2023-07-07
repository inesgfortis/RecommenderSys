# Libraries
import dash
from dash import html, callback, Input, Output, State, ctx, dcc
import dash_bootstrap_components as dbc

#from pages import dashLogin, dashRegister, dashQuiz, dashMovies

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

        # dcc.Location(id='url', refresh=False),
        # html.Div(id='page-content')

    ], fluid = True)



########################################################################################################################
# CALLBACKS
########################################################################################################################

# Callback para redirigir al hacer clic en el botón "Cerrar sesión"
# @app.callback(Output('url', 'pathname'),
#               Input('logout-button', 'n_clicks'))
# def logout(n_clicks):
#     if n_clicks:
#         # Redirige a la página de inicio de sesión
#         return '/'

# @app.callback(Output('page-content', 'children'),
#               Input('url', 'pathname'))
# def render_page_content(pathname):
#     if pathname == '/':
#         return dashLogin.layout
#     elif pathname == '/Register':
#         return dashRegister.layout
#     elif pathname == '/Quiz':
#         return dashQuiz.layout
#     elif pathname == '/Recommendations':
#         return dashMovies.layout
#     else:
#         return dbc.Alert("Página no encontrada.", color="danger")


########################################################################################################################
########################################################################################################################

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)

########################################################################################################################
########################################################################################################################


