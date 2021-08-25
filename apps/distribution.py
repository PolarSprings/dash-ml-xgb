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
hist_data = []
group_labels = []

for edu in master.typical_educational_background_for_entry.unique():
    hist_data.append(master.median_wage[master.typical_educational_background_for_entry.isin([edu])])
    group_labels.append(edu)

rowcols = [[1,1],[1,2],[2,1],[2,2],[3,1],[3,2],[4,1],[4,2]]
subplots = make_subplots(rows=4,cols=2, subplot_titles=group_labels, vertical_spacing= 0.15, x_title='Median Wage ($)',y_title='Frequency')

for subplot in range(8):
    subplots.add_histogram(name=group_labels[subplot],x=hist_data[subplot],row = rowcols[subplot][0],col = rowcols[subplot][1],xaxis='x1').update_layout(
        {'title':{'text':'Distribution of Median Wage, By Education Level','font':{'size':28},'x':0.5},'legend':{'title':{'text':'Education'}},
        'xaxis':{'range':[0,220000]},'height':600}).update_xaxes(matches='x').update_annotations({'font_size':12})


layout = html.Div([
            dcc.Graph(id='histogram-dist',
                     figure = ff.create_distplot(hist_data=[master.median_wage], group_labels=['all education'], bin_size=2000).update_layout({
                        'title':{'text':'Distribution of Median Wage, All Education Levels', 'font':{'size':28}, 'x':0.5},
                        'showlegend':False,'xaxis':{'title':{'text':'Median Wage ($)'}}, 'yaxis':{'title':{'text':'Frequency'}}, 'height':600}
               )),
            dcc.Graph(id='hist-by-edu',
                    figure = subplots
                     )
])