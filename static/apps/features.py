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

# layout
fund_asc = newfeats.sort_values(by='Fundamentals',ascending=True)
feat1 = px.scatter(fund_asc, x='Fundamentals',y='AdjSalePrice',opacity=0.5, color_discrete_sequence=px.colors.qualitative.D3)
feat1.update_layout({'title':{'text':'Feature Creation: "Fundamentals"', 'font':{'size':28}, 'x':0.5}, 
                   'xaxis':{'title':{'text':'Category'}}, 
                   'yaxis':{'title':{'text':'Price ($)'}}})

feat2 = px.scatter(newfeats, x='Details', y='AdjSalePrice', opacity=0.5, color_discrete_sequence=px.colors.qualitative.D3)
feat2.update_layout({'title':{'text':'Feature Creation: "Details"', 'font':{'size':28}, 'x':0.5}, 
                   'xaxis':{'title':{'text':'Category Score'}}, 
                   'yaxis':{'title':{'text':'Price ($)'}}})

feat3 = px.scatter_3d(newfeats,x='Location',y='Details',z='AdjSalePrice', opacity=0.5, color_discrete_sequence=px.colors.qualitative.D3)
feat3.update_layout({'title':{'text':'Sale Price by Details', 'font':{'size':28},'x':0.5}})

feat4 = px.scatter_3d(newfeats,x='Location',y='Fundamentals',z='AdjSalePrice', opacity=0.5, color='Details')
feat4.update_layout({'title':{'text':'Sale Price by Details, Fundamentals', 'font':{'size':28},'x':0.5}})

# app code

layout = html.Div([
	html.Div([
		html.H3(
			'Features',
			className='introtitle text'
			),
		html.P(
			'This section details the creation of several important variables, such as "Location", "Fundamentals", and "Details". The majority of the info contained in these variables are part of the original data as ordinal, nominal, and continuous features. Because of the structure of the data, scores tended to improve as certain variables were combined together.',
			className='intro text'
			)
		],
		className='features header'),
	dcc.Graph(id='feat1 graph',
		figure=feat1),
	dcc.Graph(id='feat2 graph',
		figure=feat2),
	dcc.Graph(id='feat3 graph',
		figure=feat3),
	dcc.Graph(id='feat4 graph',
		figure=feat4),
	])