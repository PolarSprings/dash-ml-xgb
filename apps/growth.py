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
from app import app

# read in data
repo1 = ('https://raw.githubusercontent.com/PolarSprings/EduRepos/main/bls_occupational_educational.csv')
repo2 = ('https://raw.githubusercontent.com/PolarSprings/EduRepos/main/bls_occupational_projections.csv')
repo3 = ('https://raw.githubusercontent.com/PolarSprings/EduRepos/main/bls_occupational_titles.csv')

educate = pd.read_csv(repo1, skipinitialspace=True)
project = pd.read_csv(repo2, skipinitialspace=True)
titles = pd.read_csv(repo3, skipinitialspace=True)

pd.set_option('display.max_rows',None)
master = educate.merge(project, on='occ_code').merge(titles, on='occ_code')

# groupby 
master['Change (%)'] = ((master.employment_2029 - master.employment_2019) / master.employment_2019) * 100
growth = master.groupby(['occ_title','occ_code']).agg({'Change (%)':np.mean}).sort_values(by='Change (%)',ascending=False).reset_index()

layout = html.Div([
	dcc.Graph(id='growth-bar',
	         figure=px.bar(growth[:25], y='occ_code',x='Change (%)', 
	            color='occ_title', color_discrete_sequence=px.colors.qualitative.Dark24, 
	            labels={'occ_title': 'Title of occupation'}).update_yaxes(categoryorder='total ascending').update_layout({
	    'title':{'text':'Growth by Occupation, 10 Year Change', 'font':{'size':28}, 'x':0.5}, 
	    'xaxis':{'title':{'text':'Change, 2019-2029 (%)'}}, 
	    'yaxis':{'title':{'text':'Occupation'}}}
	            ))
])