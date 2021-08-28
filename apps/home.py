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
			'I am a data analyst with a background in content strategy. My experience with data is hands on, focusing on how data can improve the product. I believe the perfect set of data exists for any strategy, and a good data analyst can find the data that helps.',
			className='intro text'
			),
		html.P(
			'The work Unsupervised is doing in the space is genuinely thrilling to me. It seems like the concept of machine learning, especially for data generation and strategy development, is helping a lot people. As a former marketing specialist with fluency in machine learning models, I would be a great fit for understanding these customer challenges and relaying them to the team.',
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