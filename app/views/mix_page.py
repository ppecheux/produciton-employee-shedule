import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_table
from app import app
from algos.production_mix import merge_mix
import numpy as np
table_colums = {"name": "text", "time": "numeric", "quantity": "numeric"}

@app.callback(
    Output('table_initial_quantity_time', 'data'),
    [Input('add_button', 'n_clicks')],
    [State('table_initial_quantity_time', 'data'),
     State('table_initial_quantity_time', 'columns')])
def add_row(n_clicks, rows, columns):
    if not n_clicks:
        raise PreventUpdate
    rows.append({c['id']: '' for c in columns})
    return rows

@app.callback(
    Output('table_suggested_order', 'data'),
    [Input('table_initial_quantity_time', 'data')]
)
def data_table_suggested_order(init_data):
    if not init_data:
        PreventUpdate

    #create a list of time needed for each product
    times = []
    for row in init_data:
        if '' not in (row['name'], row['time'], row['quantity']):
            times.extend([float(row.get('time',0))]*int(row.get('quantity',0)))

    mixed_times = merge_mix(times)
    #create data for the suggested order table
    suggested_data = []
    cumulated_time = 0
    for time in mixed_times:
        cumulated_time += time
        for row in init_data:
            if '' not in (row['name'], row['time'], row['quantity']) and int(row.get('quantity',0)) > 0 and float(row.get('time',0)) == time:
                suggested_data.append({'name': row.get('name',None), 'time': time, 'cumulated_time': cumulated_time})
                row['quantity'] -= 1

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
        {'x': list(range(len(table_data_names))), 'y': [np.mean(table_data_times)]*len(table_data_names), 'name': 'average production time'}
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
    html.H1('List of product needed to be produced'),
    dash_table.DataTable(
        id='table_initial_quantity_time',
        columns=[{'id': name, 'name': name, 'type': type} for name, type in table_colums.items()],
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

