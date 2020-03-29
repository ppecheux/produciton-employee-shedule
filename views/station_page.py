import base64
import datetime
import io
import numpy as np
import pandas as pd
from dash import callback_context
from app import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_table
import json

from algos.stations import assign_stations

table_colums = {"product": "text", "activity_block_name": "text",
                "activity_block_duration": "numeric", "fixed_station_nb": "numeric"}

@app.callback([Output('table_initial_stations', 'columns'),
               Output('table_initial_stations', 'data')],
              [Input('upload_station_data', 'contents'),
               Input('add_sation_row', 'n_clicks')],
              [State('upload_station_data', 'filename'),
               State('upload_station_data', 'last_modified'),
               State('table_initial_stations', 'data'),
               State('table_initial_stations', 'columns')])
def update_table_initial_quantity_time(contents, n_clicks, filename, date, init_data, columns):
    
    # case we want to add a row
    user_click = callback_context.triggered[0]['prop_id'].split('.')[0]
    if user_click and user_click == 'add_sation_row':
        init_data.append({c['id']: '' for c in columns})
        return [columns, init_data]
    #case we upload data
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    df.columns = map(str.lower, df.columns)
    df = df[[column for column in table_colums.keys()]]

    return [[{'name': col.lower(), 'id': col.lower()} for col in df.columns], df.to_dict('records'), ]


@app.callback(
    Output('table_suggested_order_stations', 'data'),
    [Input('table_initial_stations', 'data'),
    Input('nb_station_input', 'value')]
)
def data_table_suggested_order(init_data, nb_stations):
    if not init_data:
        raise PreventUpdate
    print(f'init data = {init_data} {type(init_data)}')
    # create a list of time needed for each product
    try:
        activities = []
        for row in init_data:
            if '' not in (row['product'], row['activity_block_name'], row['activity_block_duration']):
                row['activity_block_duration'] = float(row['activity_block_duration'])
                activities.append(row)
    except TypeError:
        raise PreventUpdate
    #print(json.dumps(activities))
    suggested_stations = assign_stations(activities, nb_stations)
    print(suggested_stations)
    if not suggested_stations:
        raise PreventUpdate
    return suggested_stations


@app.callback(
    Output('graph_suggested_order_stations', 'figure'),
    [Input('table_suggested_order_stations', 'data')]
)
def figure_graph_suggested_order(table_data):
    if not table_data:
        raise PreventUpdate
    df = pd.DataFrame.from_records(table_data)
    df.station_nb = pd.to_numeric(df.station_nb, errors='coerce')
    table_data_names = df.station_nb[~np.isnan(df.station_nb)].unique()
    if not len(table_data_names):
        raise PreventUpdate
    
    station_durations = {}
    for station in table_data_names:
        if not np.isnan(station):
            station_durations[int(station)] = df.loc[df.station_nb == station, 'activity_block_duration'].sum()
    print(station_durations)
    data = [
        {
            'x': [nb],
            'y': [duration],
            'type': 'bar',
            'name': f'station {nb}'
        } for nb, duration in station_durations.items()] + [
        {'x': list(range(len(station_durations))), 'y': [np.mean(
            list(station_durations.values()))], 'name': 'average station duration'}
    ]

    figure = {
        'data': data,
        'layout': {
            'title': 'station workload',
            'xaxis': {'title': 'rank on the production line'},
            'yaxis': {'title': 'station duration'}
        }
    }
    return figure

layout = dbc.Container([
    html.H1('Station Balancing page'),
    html.Div('enter the number of stations on the production line'),
    dcc.Input(id='nb_station_input', value=1, type='number', min=1, placeholder='number of stations'),
    html.Div('Enter the list of product needed to be produced on the same line'),
    dcc.Upload(id='upload_station_data',
               children=html.Div(
                   [
                       'Drag and Drop or ',
                       html.A('Select File'),
                       f' (csv or xls) \n must have {table_colums.keys()} columns'
                   ]
               ),
               style={
                   'width': '100%',
                   'height': '60px',
                   'lineHeight': '60px',
                   'borderWidth': '1px',
                   'borderStyle': 'dashed',
                   'borderRadius': '5px',
                   'textAlign': 'center',
                   'margin': '10px'
               },
               ),
    dash_table.DataTable(
        id='table_initial_stations',
        columns=[{'id': name, 'name': name, 'type': type}
                 for name, type in table_colums.items()],
        data=[],
        editable=True,
        row_deletable=True
    ),
    html.Button('Add row', id='add_sation_row'),
    html.H3('Suggested stations of for the activity blocks on the production line'),
    dash_table.DataTable(
        id='table_suggested_order_stations',
        columns=[
            {'id': 'product', 'name': 'product'},
            {'id': 'activity_block_name', 'name': 'activity_block_name'},
            {'id': 'activity_block_duration', 'name': 'activity_block_duration'},
            {'id': 'station_nb', 'name': 'station_nb'}
        ]
    ),
    dcc.Graph(
        id='graph_suggested_order_stations'
    )
])
