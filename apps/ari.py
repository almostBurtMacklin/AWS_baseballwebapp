import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import datetime
import numpy as np
from dash.dependencies import Input, Output
from apps import common
from app import app
import dash_table
import base64
import gc
import dash_bootstrap_components as dbc
from apps import common
from app import app

df = pd.read_csv('data/ari.csv', dtype={'b_count': 'category', 's_count' : 'category', 'pitcher_id' : 'category', 'pitch_type' : 'category', 'stand': 'category' })

teamColor = [[0, "#fff"],
                [0.25, "#d5f5f7"],
                [0.45, "#acebef"],
                [0.65, "#82e1e7"],
                [0.85, "#59d7df"],
                [1, "#30ced8"]]

darker = '#A71930'
lighter = '#E3D4Ad'
bright = '#30Ced8'

features = df.pitcher_id.unique()
pitches = df.pitch_type.unique()
opts = [{'label' : i, 'value' : i} for i in features]
tops = [{'label' : j, 'value' : j} for j in pitches]
ballsari = [{'label' : '0', 'value' : '0.0'},             #increase num
         {'label' : '1', 'value' : '1.0'},
         {'label' : '2', 'value' : '2.0'},
         {'label' : '3', 'value' : '3.0'}]

strikeari = [{'label' : '0', 'value' : '0.0'},            #increase num
         {'label' : '1', 'value' : '1.0'},
         {'label' : '2', 'value' : '2.0'}]

batterari = [{'label' : 'Right', 'value' : 'R'},          #increase num
         {'label' : 'Left', 'value' : 'L'}]

trace_1 = go.Histogram2d()

layouts = go.Layout(height = 600,
                   width = 600)
figari = go.Figure(data = [trace_1], layout = layouts)    #increase num
value = opts[0]['value']
def counts(s,b,hand,pitcher):
    pitches = df.query('pitcher_id == @pitcher').pitch_type.unique()
    j= 0
    i= 0
    bc = ['0','1','2','3']
    sc = ['0','1','2']
    final = pd.DataFrame(data = pitches, columns = ['Pitch Type'])
    for st in s:
        
        j = 0
        for ba in b:
            res = []
            total = df.query('pitcher_id == @pitcher and b_count == @ba and s_count == @st and stand == @hand').shape[0]
            for value in pitches:
                res.append(df.query('pitcher_id == @pitcher and b_count == @ba and s_count == @st and pitch_type == @value and stand == @hand').shape[0]
                       /total)
            colname = (bc[j] + '-'+ sc[i])
            #df1 = pd.DataFrame(data = res, columns = [colname])  
            final[colname] = res
            final[colname] = final[colname].multiply(100)
            final[colname] = final[colname].round(3)
            j += 1
        i += 1
    
    
    return final
b = ['0.0','1.0','2.0','3.0']
s = ['0.0','1.0','2.0']
fin = counts(s,b,'L',  opts[0]['value'] )
finR = counts(s,b,'R', opts[0]['value'])
#image_filename = 'oriole.jpg' # replace with your own image
#encoded_image = base64.b64encode(open(image_filename, 'rb').read())
gc.collect()
layout = html.Div([
                #common.get_header(),
                common.get_menu(),
                html.Div([
                    html.Div([
                        #html.Img(src='data:oriole/jpg;base64,{}'.format(encoded_image.decode()),style ={'width': '99%'}),
                        html.H1("Arizona Diamondbacks Match Up Chart - Pitcher Tendencies",
                         style = {#'backgroundColor' : '#512888',
                                 'color': lighter,
                                  'text-align' : 'center',
                                  'height': '50px',
                                  'text-shadow' : '-1px -1px 0 #fff, 1px -1px 0 #fff, -1px 1px 0 #fff, 1px 1px 0 #fff'}),
                        
                        html.P([
                            html.P("Pitcher", style={'color' : 'white'}),
                            dcc.Dropdown(id = 'opt', options = opts, value = opts[0]['value'])],
                            style = {'width': '300px',
                                            'fontSize' : '20px',
                                            'padding-left' : '5px',
                                            'display': 'inline-block'}), 
                
                        html.P([
                            html.P("Pitch Type", style={'color' : 'white'}),
                            dcc.Dropdown(id = 'pitchari', options = tops, value = tops[0]['value'])],  #increase num
                            style = {'width': '250px',
                                            'fontSize' : '20px',
                                            'padding-left' : '75px',
                                            'display': 'inline-block'}),
                        html.P([
                            html.P("Ball", style={'color' : 'white'}),
                            dcc.Dropdown(id = 'ballsari',     #increase num
                                         options = ballsari,
                                         value = ballsari[0]['value'])],

                            style = {'width': '150px',
                                            'fontSize' : '20px',
                                            'padding-left' : '75px',
                                            'display': 'inline-block'}),
                        html.P([
                            html.P("Strike", style={'color' : 'white'}),
                            dcc.Dropdown(id = 'strikeari', options = strikeari, value = strikeari[0]['value'])],  #increase num
                            style = {'width': '150px',
                                            'fontSize' : '20px',
                                            'padding-left' : '75px',
                                            'display': 'inline-block'}),
                        html.P([
                            html.P("Batter Handedness", style={'color' : 'white'}),
                            dcc.Dropdown(id = 'batterari', options = batterari, value = batterari[0]['value'])],      #increase num
                            style = {'width': '300px',
                                            'fontSize' : '20px',
                                            'padding-left' : '75px',
                                            'display': 'inline-block'}),]), ], style = {'text-align' : 'center'}),
##                html.P([
##                    dcc.Dropdown(id = 'outs', options = outs, value = outs[0]['value'])],
##                    style = {'width': '100px',
##                                    'fontSize' : '20px',
##                                    'padding-left' : '75px',
##                                    'display': 'inline-block'}),
        
                #html.Div(id='app-1-display-value'),
                #dcc.Link('Go to First', href='/first'),

                html.Div([
                    html.Div([
                        html.H3('Pitch Location Heatmap', style={'color' : 'white'}),
                        dcc.Graph(id='gari',figure = figari)],  style={                         #increase num
                                                                    "display": "block",
                                                                    "margin-left": "auto",
                                                                    "margin-right": "auto",
                                                                    "width" : "auto"
                                                                    }, className = "six columns"),
                    
                    html.Div([
                        html.H3('vs Left Handed Hitters', style={'color' : 'white'}),
                        dash_table.DataTable(
                        id='tableari',        #increase num
                        columns=[{"name": i, "id": i} for i in fin.columns],
                        data=fin.to_dict('records'),
                        style_cell={'textAlign': 'center'},
                        style_data_conditional=[ {
                                'if': {'column_id': str(x), 'filter_query': '{{{0}}} > 25 && {{{0}}} < 100'.format(x)},
                                'color': darker,
                                'backgroundColor' : lighter
                            } for x in fin.columns.to_list()
                        ], style_table={'width': '95%'}),
                        
                        html.H3('vs Right Handed Hitters', style={'color' : 'white'}),
                        dash_table.DataTable(
                        id='tableari1',        #increase num
                        columns=[{"name": i, "id": i} for i in finR.columns],
                        data=finR.to_dict('records'),
                        style_cell={'textAlign': 'center'},
                        style_data_conditional=[ {
                                'if': {'column_id': str(x), 'filter_query': '{{{0}}} > 25 && {{{0}}} < 100'.format(x)},
                                'color': darker,
                                'backgroundColor' : lighter
                            } for x in finR.columns.to_list()
                        ],
                        style_table={'width': '95%'})], className = "six columns")], className = "row")], style={
                                                                    'backgroundColor' : darker                   
                                                                    },className = "all")
                    
##                    html.Div([
##                        html.H3('vs Right Handed Hitters'),
##                        dash_table.DataTable(
##                        id='table1',
##                        columns=[{"name": i, "id": i} for i in finR.columns],
##                        data=finR.to_dict('records'),
##                        style_cell={'textAlign': 'center'},
##                        style_data_conditional=[ {
##                                'if': {'column_id': str(x), 'filter_query': '{{{0}}} > 25 && {{{0}}} < 100'.format(x)},
##                                'color': 'white',
##                                'backgroundColor' : 'rgb(111,76,179)'
##                            } for x in finR.columns.to_list()
##                        ],
##                        
##                        style_table={'width': '90%'})], className = "seven columns")], className = "r0w")
##                ], className = "all")


@app.callback(
    Output('gari', 'figure'), #increase num
    [Input('opt', 'value'),
    Input('pitchari','value'),
    Input('ballsari','value'),
    Input('strikeari','value'),
    Input('batterari', 'value')]
    )
                
def update_figure(input1, input2, input3, input4, input5):
    
    Final = df.query('pitcher_id == @input1 and pitch_type == @input2 and stand == @input5 and b_count == @input3 and s_count == @input4')
    
    trace_2 = go.Histogram2d(x = Final.px, y = Final.pz, colorscale=teamColor ,
                reversescale = False)
    fig = go.Figure(data = [trace_2], layout = layouts)
    fig.layout.update(
            title = go.layout.Title(
                text = "View From Catcher's Viewpoint"),
            xaxis = go.layout.XAxis(
                title=go.layout.xaxis.Title(
                text="Distance From Center of Home Plate (in feet)")),
            yaxis = go.layout.YAxis(
                title=go.layout.yaxis.Title(
                text = "Distance From Ground (in feet, negative means it bounced)")),
        shapes=[
            # unfilled Rectangle
            go.layout.Shape(
                type="rect",
                x0=-.7083,
                y0=1.56,
                x1=.7083,
                y1=3.435,
                line=dict(
                    color="Black",
                ))])
    gc.collect()
    return fig


@app.callback(
    Output('tableari', 'data'),       #increase num
    [Input('opt', 'value'),
    Input('pitchari','value')])
def update_table_Left(pitcher, value):
    pitches = df.query('pitcher_id == @pitcher').pitch_type.unique()
    j= 0
    i= 0
    bc = ['0','1','2','3']
    sc = ['0','1','2']
    final = pd.DataFrame(data = pitches, columns = ['Pitch Type'])
    for st in s:
        
        j = 0
        for ba in b:
            res = []
            total = df.query('pitcher_id == @pitcher and b_count == @ba and s_count == @st and stand == "L"').shape[0]
            for value in pitches:
                res.append(df.query('pitcher_id == @pitcher and b_count == @ba and s_count == @st and pitch_type == @value and stand == "L"').shape[0]
                       /total)
            colname = (bc[j] + '-'+ sc[i])
            #df1 = pd.DataFrame(data = res, columns = [colname])  
            final[colname] = res
            final[colname] = final[colname].multiply(100)
            final[colname] = final[colname].round(3)
            j += 1
        i += 1
    
    gc.collect()
    return final.to_dict('records')
@app.callback(
    Output('tableari1', 'data'),       #increase num
    [Input('opt', 'value'),
    Input('pitchari','value')])
def update_table_Right(pitcher, value):
    pitches = df.query('pitcher_id == @pitcher').pitch_type.unique()
    j= 0
    i= 0
    bc = ['0','1','2','3']
    sc = ['0','1','2']
    final = pd.DataFrame(data = pitches, columns = ['Pitch Type'])
    for st in s:
        
        j = 0
        for ba in b:
            res = []
            total = df.query('pitcher_id == @pitcher and b_count == @ba and s_count == @st and stand == "R"').shape[0]
            for value in pitches:
                res.append(df.query('pitcher_id == @pitcher and b_count == @ba and s_count == @st and pitch_type == @value and stand == "R"').shape[0]
                       /total)
            colname = (bc[j] + '-'+ sc[i])
            #df1 = pd.DataFrame(data = res, columns = [colname])  
            final[colname] = res
            final[colname] = final[colname].multiply(100)
            final[colname] = final[colname].round(3)
            j += 1
        i += 1
    
    gc.collect()
    return final.to_dict('records')
@app.callback(
    Output('pitchari', 'options'),        #increase num
    [Input('opt', 'value')])
def update_dropdown(input1):
    pitchTypes = df.query('pitcher_id == @input1').pitch_type.unique()
    return [{'label' : j, 'value' : j} for j in pitchTypes]
    
gc.collect()

if __name__ == '__main__':
    app.run_server(debug=True)



# https://community.plot.ly/t/two-graphs-side-by-side/5312