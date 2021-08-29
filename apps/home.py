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

layout = html.Div([
		html.Div([
	# header
			html.Div([

				html.Div([	
					html.A([
				        html.Img(src=app.get_asset_url('Profile.png'),
				            className='img'),
				        ],href='https://linkedin.com/in/benjaminbnoyes',
				        target='_blank',
				        className='imgcont',
						),
					html.H3(
						'Ben Noyes',
						className='introtitle text'
						),
					], className='imgsplitchild'),

				html.Div([	
					html.A([
				        html.Img(src=app.get_asset_url('Unsupervised-2.png'),
				            className='img'),
				        ],href='https://unsupervised.com/careers/jobs?gh_jid=5398780002',
				        target='_blank',
				        className='imgcont',
						),
					html.H3(
						'Unsupervised',
						className='introtitle text'
						),
					], className='imgsplitchild'),

			], className='imgsplit'),

		html.Hr(),
		html.P(
			'I am a data scientist with a preference for classification. In my work, I use tree based models to set and deliver solid numerical predictions based on clusters. I believe the perfect set of data exists for any situation, and that the only challenge is to find it.',
			className='intro text'
			),
		html.P(
			"""AI that can make predictions is something fairly new to the world of machine learning - as far as application goes, it's still quite new. I would be interested int joining the client side to explore these results,  communicating with the team on how they shape the journey of the client. With my background working across teams at Alibaba, I would be a great fit for the role.""",
			className='intro text'
			),
		html.Hr(),
		html.H4(
			'Plotly'
			),
		html.P(
			'This dashboard uses machine learning to predict the prices of homes in Aimes, Iowa. Full stack used for this example: pandas, scikit-learn, plotly / dash, xgboost.',
			className='intro text'
			)
	],
	className='features header home'),
	html.P(
		"Data Analytics portfolio, advanced analytics. Select from the menu.",
		className='botright'),
	],
	)