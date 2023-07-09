# Libraries
import dash
from dash import html
import dash_bootstrap_components as dbc

## App
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.JOURNAL],suppress_callback_exceptions=True, title="TFG", use_pages=True)

app.layout = dbc.Container(
    children = [
        html.Div(id ="dash-content",children = dash.page_container),
    ], 
    fluid = True
)

########################################################################################################################
########################################################################################################################

server = app.server

if __name__ == '__main__':
    app.run_server(debug=False)

########################################################################################################################
########################################################################################################################


