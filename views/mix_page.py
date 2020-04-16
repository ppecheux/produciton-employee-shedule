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


from algos.production_mix import merge_mix


table_colums = {"name": "text", "time": "numeric", "quantity": "numeric"}


@app.callback([Output('table_initial_quantity_time', 'columns'),
               Output('table_initial_quantity_time', 'data')],
              [Input('upload_mix_data', 'contents'),
               Input('add_button', 'n_clicks')],
              [State('upload_mix_data', 'filename'),
               State('upload_mix_data', 'last_modified'),
               State('table_initial_quantity_time', 'data'),
               State('table_initial_quantity_time', 'columns')])
def update_table_initial_quantity_time(contents, n_clicks, filename, date, init_data, columns):
    
    # case we want to add a row
    print(columns)
    user_click = callback_context.triggered[0]['prop_id'].split('.')[0]
    if user_click and user_click == 'add_button':
        init_data.append({c['id']: '' for c in columns})
        return [columns, init_data]
    print('upload')
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
    Output('table_suggested_order', 'data'),
    [Input('table_initial_quantity_time', 'data')]
)
def data_table_suggested_order(init_data):
    if not init_data:
        raise PreventUpdate

    # create a list of time needed for each product
    try:
        times = []
        for row in init_data:
            if '' not in (row['name'], row['time'], row['quantity']):
                times.extend(
                    [float(row.get('time', 0))] * int(row.get('quantity', 0))
                )
    except TypeError:
        raise PreventUpdate

    mixed_times = merge_mix(times)
    # create data for the suggested order table
    suggested_data = []
    cumulated_time = 0
    for time in mixed_times:
        cumulated_time += time
        for row in init_data:
            if '' not in (row['name'], row['time'], row['quantity']) and int(row.get('quantity', 0)) > 0 and float(row.get('time', 0)) == time:
                suggested_data.append(
                    {'name': row.get('name', None), 'time': time,
                     'cumulated_time': cumulated_time}
                )
                row['quantity'] = int(row['quantity']) - 1

    return suggested_data


@app.callback(
    Output('graph_suggested_order', 'figure'),
    [Input('table_suggested_order', 'data')]
)
def figure_graph_suggested_order(table_data):
    if not table_data:
        raise PreventUpdate

    table_data_names = [row['name'] for row in table_data]
    table_data_times = [float(row['time']) for row in table_data]
    data = [
        {
            'x': [indice for indice, v in enumerate(table_data_names) if v == name],
            'y': [table_data_times[table_data_names.index(name)]]*table_data_names.count(name),
            'type': 'bar',
            'name': name
        } for name in set(table_data_names)] + [
        {'x': list(range(len(table_data_names))), 'y': [np.mean(
            table_data_times)]*len(table_data_names), 'name': 'average production time'}
    ]

    figure = {
        'data': data,
        'layout': {
            'title': 'order of production visualization',
            'xaxis': {'title': 'rank on the production line'},
            'yaxis': {'title': 'production time'}
        }
    }
    return figure


layout = dbc.Container([
    html.H1('List of product needed to be produced',style={'color':'red'}),
    dcc.Upload(id='upload_mix_data',
               children=html.Div(
                   [
                       'Drag and Drop or ',
                       html.A('Select File'),
                       ' (csv or xls) \n must have name, time and quantity columns'
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
        id='table_initial_quantity_time',
        columns=[{'id': name, 'name': name, 'type': type}
                 for name, type in table_colums.items()],
        data=[],
        editable=True,
        row_deletable=True
    ),
    html.Button('Add row', id='add_button'),
    html.H1('Suggested order of products on the production line'),
    dash_table.DataTable(
        id='table_suggested_order',
        columns=[
            {'id': 'name', 'name': 'name'},
            {'id': 'time', 'name': 'time'},
            {'id': 'cumulated_time', 'name': 'cumulated_time'}
        ]
    ),
    dcc.Graph(
        id='graph_suggested_order'
    )
])
