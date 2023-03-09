# -*- coding: utf-8 -*-

import plotly.graph_objects as go

import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import warnings
warnings.filterwarnings('ignore')
pd.options.display.float_format = '{:,}'.format

app = dash.Dash(__name__)
server = app.server

path = 'https://raw.githubusercontent.com/garygillespie9/tobacco_data/main/Food_Sec_Calc.csv'
df = pd.read_csv(path)

df.head(7)

df2 = df[['Area', 'Tobacco Area']]
print(df2.sort_values(by=['Tobacco Area']).tail(25))

df.loc[(df.Area == 'Philippines'), 'ISO3_CODE'] = 'PHL'

selected_crop = 'Pulse'
N_countries = (df['% ' + str(selected_crop)+' demand'] >= 100).sum()
print(N_countries)

# Cereal Amounts
idx1 = 0
df['Cereal Amount'] = ''
amount = list()
for each in df['Cereal Security']:
    if each == 'None':
        tonnes = 0
        amount.append(tonnes)
    else:
        tonnes = ((df[str(each) + ' Yield'].iloc[idx1]) * (df['Tobacco Area']/2).iloc[idx1]).round(2)
        amount.append(tonnes)
    idx1 += 1
df['Cereal Amount'] = amount

# Pulse Amounts
idx2 = 0
df['Pulse Amount'] = ''
amount = list()
for each in df['Pulse Security']:
    if each == 'None':
        tonnes = 0
        amount.append(tonnes)
    else:
        tonnes = ((df[str(each) + ' Yield'].iloc[idx2]) * (df['Tobacco Area']/6).iloc[idx2]).round(2)
        amount.append(tonnes)
    idx2 += 1
df['Pulse Amount'] = amount

# Breakcrop Amount
idx3 = 0
df['Breakcrop Amount'] = ''
amount = list()
for each in df['Breakcrop Security']:
    if each == 'None':
        tonnes = 0
        amount.append(tonnes)
    else:
        tonnes = ((df[str(each) + ' Yield'].iloc[idx3]) * (df['Tobacco Area']/6).iloc[idx3]).round(2)
        amount.append(tonnes)
    idx3 += 1
df['Breakcrop Amount'] = amount

df1 = df[['Area', 'ISO3_CODE', 'Breakcrop Security', '% Breakcrop demand']]
print(df1.sort_values(by=['% Breakcrop demand']).tail(25))

# Root Crop Amount
idx4 = 0
df['Root Amount'] = ''
amount = list()
for each in df['Root Security']:
    if each == 'None':
        tonnes = 0
        amount.append(tonnes)
    else:
        tonnes = ((df[str(each) + ' Yield'].iloc[idx4]) *
                  (df['Tobacco Area']/6).iloc[idx4]).round(2)
        amount.append(tonnes)
    idx4 += 1
df['Root Amount'] = amount


app.layout = html.Div([
    html.H1("Amount of Crops that Could be Produced Using Land Currently Cultivating Tobacco",
            style={'text-align': 'center'}),
    dcc.Dropdown(id='select_crop',
                 options=[
                     {'label': 'Cereal Crops', 'value': 'Cereal'},
                     {'label': 'Pulse Crops', 'value': 'Pulse'},
                     {'label': 'Break Crops', 'value': 'Breakcrop'},
                     {'label': 'Root Crops', 'value': 'Root'}],
                 multi=False,
                 value='Cereal',
                 style={'width': "40%"}
                 ),
                 html.Div(id='output_container', children=[]),
                 html.Br(),
                 html.Div(id='output_container1', children=[]),
                 html.Br(),
                 dcc.Graph(id='tobacco_graph', figure={}, style={'width': '90vw', 'height': '90vh'})
])


@app.callback(
    [
        Output(component_id='output_container', component_property='children'),
        Output(component_id='output_container1', component_property='children'),
        Output(component_id='tobacco_graph', component_property='figure')],
        [Input(component_id='select_crop', component_property='value')]
)
def update_graph(option_selected):
    """Creates the map to show on the web service"""
    N_countries = (df['% ' + str(option_selected)+' demand'] >= 100).sum()
    container1 = 'Crop type chosen is: {}'.format(option_selected)
    container2 = 'Number of countries that can offset >= 100% of their imports for {} crops is {}'\
        .format(option_selected, N_countries)
    dff = df.copy()
    fig = go.Figure(data=go.Choropleth(
                    locations=dff['ISO3_CODE'],
                    z=dff['% ' + str(option_selected) + ' demand'],
                    colorscale='spectral',
                    colorbar_title='% of traded value',
                    text=dff.apply(lambda row: f"{'Country: '+row['Area']} <br> "
                                               f"{'Crop: '+row[str(option_selected)+' Security']}<br>"
                                               f"{'Amount: '+str(row[str(option_selected)+' Amount'])+'t'}<br>"
                                               f" {'Portion of traded amount: '+str(row['% '+str(option_selected)+' demand'])+'%'}", axis=1),
                    hoverinfo="text"
                    ))
    fig.update_traces(zmin=-100, zmax=100)
    fig.update_layout(margin=dict(l=10, r=0, t=10, b=10))
    return container1, container2, fig


fig = go.Figure(data=go.Choropleth(
    locations=df['ISO3_CODE'],
    z=df['% Cereal demand'],
    colorscale='spectral',
    colorbar_title='% of traded value',
    text=df.apply(lambda row: f"{'Country: '+row['Area']}<br>"
                              f" {'Crop: '+row['Cereal Security']}<br>"
                              f" {'Amount: ' + str(row['Cereal Amount'])+'t'}<br>"
                              f" {'Portion of traded amount: '+str(row['% Cereal demand'])+'%'}", axis=1),
    hoverinfo="text"
))
fig.update_traces(zmin=-100, zmax=100)
fig.update_layout(margin=dict(l=10, r=0, b=10, t=10))
fig.show()

fig = go.Figure(data=go.Choropleth(
    locations=df['ISO3_CODE'],
    z=df['% Pulse demand'],
    colorscale='spectral',
    colorbar_title='% of traded value',
    text=df.apply(lambda row: f"{'Country: '+row['Area']}<br>"
                              f" {'Crop: '+row['Pulse Security']}<br>"
                              f" {'Amount: '+str(row['Pulse Amount'])+'t'}<br>"
                              f" {'Portion of traded amount: '+str(row['% Pulse demand'])+'%'}", axis=1),
    hoverinfo="text"
))
fig.update_traces(zmin=-100, zmax=100)
fig.update_layout(margin=dict(l=10, r=0, b=10, t=10))
fig.show()

fig = go.Figure(data=go.Choropleth(
    locations=df['ISO3_CODE'],
    z=df['% Root demand'],
    colorscale='spectral',
    colorbar_title='% of traded value',
    text=df.apply(lambda row: f"{'Country: '+row['Area']}<br>"
                              f" {'Crop: '+row['Root Security']}<br>"
                              f" {'Amount: '+str(row['Root Amount'])+'t'}<br>"
                              f" {'Portion of traded amount: '+str(row['% Root demand'])+'%'}", axis=1),
    hoverinfo="text"
))
fig.update_traces(zmin=-100, zmax=100)
fig.update_layout(margin=dict(l=10, r=0, b=10, t=10))
fig.show()

fig = go.Figure(data=go.Choropleth(
    locations=df['ISO3_CODE'],
    z=df['% Breakcrop demand'],
    colorscale='spectral',
    colorbar_title='% of traded value',
    text=df.apply(lambda row: f"{'Country: '+row['Area']}<br>"
                              f" {'Crop: '+row['Breakcrop Security']}<br>"
                              f" {'Amount: '+str(row['Breakcrop Amount'])+'t'}<br>"
                              f" {'Portion of traded amount: '+str(row['% Breakcrop demand'])+'%'}", axis=1),
    hoverinfo="text"
))
fig.update_traces(zmin=-100, zmax=100)
fig.update_layout(margin=dict(l=10, r=0, b=10, t=10))
fig.show()

if __name__ == '__main__':
    app.run_server(debug=False)
