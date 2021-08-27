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
import xgboost as xgb

from app import app

# read in data
repo2 = ('C:/Users/benno/OneDrive/Python/Dash/Template - withouttopbar/assets/Data/model_selec_dim.csv')
repo4 = ('C:/Users/benno/OneDrive/Python/Dash/Template - withouttopbar/assets/Data/train_scores.csv')

simpledim = pd.read_csv(repo2, skipinitialspace=True)
scoring = pd.read_csv(repo4, skipinitialspace=True)


pd.set_option('display.max_rows',None)

data = simpledim.drop(['AdjSalePrice'], 1)
target = simpledim[['AdjSalePrice']].squeeze()

# layout

xgbooster = xgb.XGBRegressor()
idx = np.random.choice(range(0,len(simpledim)), size=round(len(simpledim)*0.95), replace=False)

x_train = data.iloc[idx]
y_train = target.iloc[idx]

x_test = data.iloc[data.index.difference(idx)]
y_test = target.iloc[data.index.difference(idx)]

xgbooster.fit(x_train, y_train)

actuals = y_test
predictions = xgbooster.predict(x_test)
residuals = actuals - predictions
x_axis = np.array(range(len(actuals)))

residsline = make_subplots(1,1)
residsline.add_scatter(x=x_axis, y=actuals, name='Actuals', mode='lines+markers', marker={'opacity':0.3,'color':'#1f77b4'})
residsline.add_scatter(x=x_axis, y=predictions, name='Predictions', mode='lines+markers', marker={'opacity':0.3,'color':'#ff7f0e' })
residsline.update_layout({'title':{'text':'Actuals x Predictions', 'font':{'size':28},'x':0.5},
                  'xaxis':{'title':{'text':'Index'}},
                  'yaxis':{'title':{'text':'Price ($)'}}})

residsdots = make_subplots(1,1)

residsdots.add_bar(x=x_axis, y=y_train, name='Prices', marker={'opacity':0.3,'color':'#1f77b4'})
residsdots.add_scatter(x=x_axis, y=residuals, mode='markers', name='Residuals', marker={'color':'#ff7f0e'})
residsdots.update_layout({'title':{'text':'Residuals x Prices', 'font':{'size':28},'x':0.5},
                  'xaxis':{'title':{'text':'Index'}},
                  'yaxis':{'title':{'text':'Price ($)'}}})

trainscores = px.scatter(scoring, x='index', y='train_scores', color_discrete_sequence=px.colors.qualitative.D3)
trainscores.update_layout({'title':{'text':'Train scores', 'font':{'size':28},'x':0.5},
                  'xaxis':{'title':{'text':'Train index'}},
                  'yaxis':{'title':{'text':'R2'}}})

# app code

layout = html.Div([
    html.Div([
        html.H3(
            'Scoring',
            className='introtitle text'
            ),
        html.P(
            "The final data for this model went through dimensionality reduction with PCA, which simplified the original data from 250 dimensions to around 10-15. We also examined new clustering methods, including unsupervised methods such as DBSCAN, as a potential alternative to more standard reduction techniques. This allowed us to compare both linear and tree-based models, to achieve R2 scores of 99% for train and 90% for test sets. As this was a regression problem and not a classification problem, given more time, we would consider opening up the data to original dimensionality as well as to more fine-tuned segmentation, which could both reduce overfitting and create a more accurate model. After hyperparameter tuning, RMSE was 21,231 which we felt was acceptable given the data at hand.",
            className='intro text'
            ),
        html.P(
            "Zoom in to see how the predictions tie in to the actuals.",
            className='intro text'
            ),
        ],
        className='inflation header'),

    dcc.Graph(id='residsline',
        figure=residsline),
    dcc.Graph(id='residsdots',
        figure=residsdots),
    dcc.Graph(id='trainscores',
        figure=trainscores),
    ])