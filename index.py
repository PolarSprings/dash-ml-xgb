import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import home, features, inflation, scoring

sidebar = html.Div(
    [
        html.H2("Data Analyst", className="display-4"),
        html.Hr(),
        html.P(
            "Using data from customers to improve the product", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact", external_link=True),
                dbc.NavLink("Features", href="/features", active="exact", external_link=True),
                dbc.NavLink("Inflation", href="/inflation", active="exact", external_link=True),
                dbc.NavLink("Scoring", href="/scoring", active="exact", external_link=True),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="SIDEBAR_STYLE",
)


content = html.Div(id="page-content", children=[], className="CONTENT_STYLE")

app.layout = html.Div([
    dcc.Location(id="url", refresh=True),
    sidebar,
    content
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/":
        return home.layout
    elif pathname == '/features':
        return features.layout
    elif pathname == '/inflation':
        return inflation.layout
    elif pathname == '/scoring':
        return scoring.layout
    else:
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognized..."),
            ]
        )


if __name__ == '__main__':
    app.run_server(debug=False, 
        host='0.0.0.0'
        # port='8050'
        )