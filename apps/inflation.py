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

# layout
import plotly.figure_factory as ff

hist = ff.create_distplot([orighousing.AdjSalePrice, orighousing.SalePrice], ['AdjSalePrice', 'SalePrice'], bin_size=1000)
hist.update_layout({'title':{'text':'Sales Price, Before and After Adjustment', 'font':{'size':28}, 'x':0.5}, 
                   'xaxis':{'title':{'text':'Price ($)'}}, 
                   'yaxis':{'title':{'text':'Frequency'}}})

box = px.box(orighousing, x='YrSold',y='SalePrice', color_discrete_sequence=['#ff7f0e'])
box.update_layout({'title':{'text':'Sale Price by Year', 'font':{'size':28}, 'x':0.5}, 
                   'xaxis':{'title':{'text':'Year Sold'}}, 
                   'yaxis':{'title':{'text':'Price ($)'}}})

eps = 550
min_samples = 13.5
lab = DBSCAN(eps=eps, min_samples=min_samples).fit(data)
simpledim['DBSCAN'] = lab.labels_
dbs = px.scatter(simpledim, x='QualScore',y='AdjSalePrice', color='DBSCAN',opacity=0.5, facet_col='DBSCAN', trendline='ols')
dbs.update_layout({'title':{'text':'Adjusted Sale Price, by Cluster', 'font':{'size':28}, 'x':0.5}, 
                   'xaxis':{'title':{'text':'Year Sold'}}, 
                   'yaxis':{'title':{'text':'Price ($)'}}})

agg = px.scatter(simpledim, x='QualScore',y='AdjSalePrice', color='DBSCAN',opacity=0.5, trendline='ols')
agg.update_layout({'title':{'text':'Adjusted Sale Price, Aggregate', 'font':{'size':28}, 'x':0.5}, 
                   'xaxis':{'title':{'text':'Year Sold'}}, 
                   'yaxis':{'title':{'text':'Price ($)'}}})

# app code

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
	dcc.Graph(id='hist',
		figure=hist),
	dcc.Graph(id='box',
		figure=box),
	dcc.Graph(id='dbs',
		figure=dbs),
	dcc.Graph(id='agg',
		figure=agg),
	])