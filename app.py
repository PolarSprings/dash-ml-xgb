import dash
import dash_bootstrap_components as dbc
from whitenoise import WhiteNoise

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.MINTY],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally=True
server = app.server
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/')
