import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import growth, wage, education, distribution

# app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     html.Div([
#         dcc.Link('Video Games|', href='/apps/vgames'),
#         dcc.Link('Other Products', href='/apps/global_sales'),
#     ], className="row"),
#     html.Div(id='page-content', children= [])
# ])


SIDEBAR_STYLE = {
    "font-family": "Times New Roman",
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "19rem",
    "padding": "2rem 1rem",
    "background-color": "#009986",
    "color":"white"
}

CONTENT_STYLE = {
    "position": "relative",
    "top": 0,
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 3rem",
}


sidebar = html.Div(
    [
        html.H2("Leif", className="display-2"),
        html.Hr(),
        html.P(
            "Analysis of occupations in the future, by growth, wage, and education", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Growth", href="/", active="exact"),
                dbc.NavLink("Wage", href="/wage", active="exact"),
                dbc.NavLink("Education", href="/education", active="exact"),
                dbc.NavLink("Distribution", href="/distribution", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    sidebar,
    content
])


# content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/":
        return growth.layout
    elif pathname == '/wage':
        return wage.layout
    elif pathname == '/education':
        return education.layout
    elif pathname == '/distribution':
        return distribution.layout

    # elif pathname == '/apps/vgames':
    #     return vgames.layout
    # elif pathname == '/apps/global_sales':
    #     return global_sales.layout
    else:
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )


if __name__ == '__main__':
    app.run_server(debug=False, port=8000, 
        # host='0.0.0.0'
        )