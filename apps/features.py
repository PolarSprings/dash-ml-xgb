import pandas as pd
import numpy as np

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State


import plotly.express as px
from plotly.offline import *
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

from app import app

# read in data
repo3 = ('https://raw.githubusercontent.com/PolarSprings/dash-ml-xgb/master/assets/Data/feature_creation.csv')

newfeats = pd.read_csv(repo3, skipinitialspace=True)

pd.set_option('display.max_rows',None)

data = newfeats.drop(['AdjSalePrice'], 1)
target = newfeats[['AdjSalePrice']].squeeze()
fund_asc = newfeats.sort_values(by='Fundamentals',ascending=True)

# layout

layout = html.Div([
	html.Div([
		html.H3(
			'Features',
			className='introtitle text'
			),
		html.P(
			'This section details the creation of several important variables, such as "Location", "Fundamentals", and "Details". The majority of the info contained in these variables are part of the data as categorical and continuous features, but because of the structure of the data, some scores tended to improve as these variables were combined together.',
			className='intro text'
			)
		],
		className='features header'),

	dcc.Dropdown(id='dropdown-feateng',
                 options=[{'label': x, 'value': x} for x in ['Fundamentals','Location','Details']],
                 value='Location'),
	dcc.Graph(id='graph-feateng', className='graph', figure={}),
	dcc.Checklist(id='checklist-withfund', options=[{'label': 'Add new feature: "Fundamentals"', 'value': 'Fundamentals'}],
				value=[], className='checklist'),
	dcc.Graph(id='graph-withfund', className='graph', figure={}),
	])

# callbacks

@app.callback(
   Output(component_id='graph-feateng', component_property='figure'),
   [Input(component_id='dropdown-feateng', component_property='value')])
def update_feateng(val_chosen):
    if len(val_chosen) > 0:
    	feat = px.scatter(newfeats, x=val_chosen, y='AdjSalePrice', opacity=0.5, color_discrete_sequence=px.colors.qualitative.D3)
    	feat.update_layout({'title':{'text':f'Feature Engineering: {val_chosen}', 'font':{'size':28}, 'x':0.5},'yaxis':{'title':{'text':'Price ($)'}},'showlegend':False})
    	return feat
    elif len(val_chosen) == 0:
        raise dash.exceptions.PreventUpdate

@app.callback(
   Output(component_id='graph-withfund', component_property='figure'),
   [Input(component_id='checklist-withfund', component_property='value')])
def update_details3d(with_fund):
    if 'Fundamentals' in with_fund:
    	feat3d = px.scatter_3d(newfeats,x='Location',y='Fundamentals',z='AdjSalePrice', opacity=0.5, color='Details')
    	feat3d.update_layout({'title':{'text':'Adjusted Sale Price, With Fundamentals', 'font':{'size':28},'x':0.5}})
    	return feat3d
    else:
    	feat3d = px.scatter_3d(newfeats,x='Location',y='Details',z='AdjSalePrice', opacity=0.5, color_discrete_sequence=px.colors.qualitative.D3)
    	feat3d.update_layout({'title':{'text':'Adjusted Sale Price', 'font':{'size':28},'x':0.5}})
    	return feat3d




 