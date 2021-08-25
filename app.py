import dash
import dash_bootstrap_components as dbc

app = dash.Dash(name, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.MINTY],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
app.config.suppress_callback_exceptions = True
server = app.server