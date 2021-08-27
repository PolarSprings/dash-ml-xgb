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
repo1 = ('C:/Users/benno/OneDrive/Python/Dash/Template - withouttopbar/assets/Data/housing_sparse_matrices.csv')
repo2 = ('C:/Users/benno/OneDrive/Python/Dash/Template - withouttopbar/assets/Data/model_selec_dim.csv')
repo3 = ('C:/Users/benno/OneDrive/Python/Dash/Template - withouttopbar/assets/Data/feature_creation.csv')

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
			'The cost of housing between 2005 and 2010 different greatly by year. One challenge within this analysis was how to best compare a house bought in 2010 with a house bought in 2006, when the financial crisis hit. This strategy took into account this change in prices by year and month, keeping in mind these ordinal features likely had some correlation in the original data. After this, we decided to look into the role of inflation, as houses bought earlier benefited from a better price. We standardized these prices by the inflation index and updated our dependent variable to reflect an adjusted sales price. This freed up our analysis to focus more on classification as our baseline measurement.',
			className='intro text'
			)
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