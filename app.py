import dash
import dash_bootstrap_components as dbc
from whitenoise import WhiteNoise
from newrelic import agent
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.MINTY])
app = agent.WSGIApplicationWrapper(app)
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally=True
server = app.server
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/')
