# Importamos las librerias mínimas necesarias
import dash
from dash import html, callback, Input, Output, State, ctx
import dash_bootstrap_components as dbc
#from dash import redirect


#from dash_bootstrap_templates import ThemeSwitchAIO

## App
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.JOURNAL], use_pages=True)
app.title="TFG"


app.layout = dbc.Container(
    children = [
        html.Br(),
        html.H1("Recommender Systems",style={'fontSize': 44}),
        html.Hr(),

        ## COMPONENTES INTERACTIVAS
        #ThemeSwitchAIO(aio_id="theme", themes=[dbc.themes.MINTY, dbc.themes.CYBORG]),
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

    ], fluid = True)


########################################################################################################################
########################################################################################################################

if __name__ == '__main__':
    app.run_server(debug=True)

########################################################################################################################
########################################################################################################################


