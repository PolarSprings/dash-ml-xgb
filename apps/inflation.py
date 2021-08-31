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

from sklearn.cluster import DBSCAN

from app import app

# read in data
repo1 = ('https://raw.githubusercontent.com/PolarSprings/dash-ml-xgb/master/assets/Data/housing_sparse_matrices.csv')
repo2 = ('https://raw.githubusercontent.com/PolarSprings/dash-ml-xgb/master/assets/Data/model_selec_dim.csv')
repo3 = ('https://raw.githubusercontent.com/PolarSprings/dash-ml-xgb/master/assets/Data/feature_creation.csv')

orighousing = pd.read_csv(repo1, skipinitialspace=True)
simpledim = pd.read_csv(repo2, skipinitialspace=True)
newfeats = pd.read_csv(repo3, skipinitialspace=True)

pd.set_option('display.max_rows',None)

data = simpledim.drop(['AdjSalePrice'], 1)
target = simpledim[['AdjSalePrice']].squeeze()

eps = 550
min_samples = 13.5
lab = DBSCAN(eps=eps, min_samples=min_samples).fit(data)
simpledim['DBSCAN'] = lab.labels_

# layout

box = px.box(orighousing, x='YrSold',y='SalePrice', color_discrete_sequence=['#739ae4'])
box.update_layout({'title':{'text':'Sale Price by Year', 'font':{'size':28}, 'x':0.5}, 
                   'xaxis':{'title':{'text':'Year Sold'}}, 
                   'yaxis':{'title':{'text':'Price ($)'}}})

dbs = px.scatter(simpledim, x='QualScore',y='AdjSalePrice', color='DBSCAN',opacity=0.5, facet_col='DBSCAN', trendline='ols', color_continuous_scale='dense')
dbs.update_layout({'title':{'text':'Adjusted Sale Price, by Cluster', 'font':{'size':28}, 'x':0.5}, 
                   'xaxis':{'title':{'text':'Year Sold'}}, 
                   'yaxis':{'title':{'text':'Price ($)'}}})

agg = px.scatter(simpledim, x='QualScore',y='AdjSalePrice', color='DBSCAN',opacity=0.5, trendline='ols', color_continuous_scale='dense')
agg.update_layout({'title':{'text':'Adjusted Sale Price, Aggregate', 'font':{'size':28}, 'x':0.5}, 
                   'xaxis':{'title':{'text':'Year Sold'}}, 
                   'yaxis':{'title':{'text':'Price ($)'}}})

# layout

layout = html.Div([
	html.Div([
		html.H3(
			'Inflation',
			className='introtitle text'
			),
		html.P(
			'The cost of housing between 2005 and 2010 differed greatly by year.',
			className='intro text'
			),
		html.Ul([
			html.Li('The cost of a house in 2010 was different than the cost of that same house in 2006. This financial crisis rocked the housing market and prices were likely considerably different.',className='intro text'),
			html.Li('The features Year Sold and Month Sold were valuable pieces of data, that helped us determine averages by year. We kept this data as "circular scales".',className='intro text'),
			html.Li('We also considered the role of inflation. To be specific, we standardized the dependent variable so that it could be interpreted across time.',className='intro text'),
			]),
		],
		className='inflation header'),
	dcc.Dropdown(id='dropdown-infl', multi=True,
                 options=[{'label': x, 'value': x} for x in ['AdjSalePrice', 'SalePrice']],
                 value=['SalePrice']),
	dcc.Graph(id='graph-distplot', className='graph', figure={}),
	dcc.Graph(className='graph',figure=box),
	dcc.Graph(className='graph',figure=dbs),
	dcc.Graph(className='graph',figure=agg),
	])

# callbacks

@app.callback(
   Output(component_id='graph-distplot', component_property='figure'),
   [Input(component_id='dropdown-infl', component_property='value')])
def update_ff(sales_price):
    if len(sales_price) > 0:
    	hist = ff.create_distplot([orighousing[str(x)] for x in sales_price],group_labels=[x for x in sales_price], bin_size=1000, colors=['#78c2ad','hotpink'])
    	hist.update_layout({'title':{'text':'Sales Price, Before and After Adjustment', 'font':{'size':28}, 'x':0.5}, 'xaxis':{'title':{'text':'Price ($)'}}})
    	return hist
    elif len(sales_price) == 0:
        raise dash.exceptions.PreventUpdate
