import datetime
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
from views.functions_for_views.functions_for_callbacks import update_table_from_upload, data_table_nb_products
from views.functions_for_views.input_components import takt_time_input

from algos.stations import assign_stations
from algos.stations import activities_weighted_avg

table_colums = {"product": "text", "activity_block_name": "text",
                "activity_block_duration": "numeric", "fixed_station_nb": "numeric"}


@app.callback([Output('table_initial_stations', 'columns'),
               Output('table_initial_stations', 'data')],
              [Input('upload_station_data', 'contents'),
               Input('add_sation_row', 'n_clicks')],
              [State('upload_station_data', 'filename'),
               State('table_initial_stations', 'data'),
               State('table_initial_stations', 'columns')])
def update_table_initial_quantity_time(contents, n_clicks, filename, init_data, columns):

    # case we want to add a row
    user_click = callback_context.triggered[0]['prop_id'].split('.')[0]
    if user_click and user_click == 'add_sation_row':
        init_data.append({c['id']: '' for c in columns})
        return [columns, init_data]
    # case we upload data
    return update_table_from_upload(contents, filename, table_colums)


@app.callback(
    Output('table_nb_products', 'data'),
    [Input('table_initial_stations', 'data')],
    [State('table_nb_products', 'data')]
)
def data_table_nb_products_stations(table_initial_stations, table_nb_products):
    return data_table_nb_products(table_initial_stations, table_nb_products)


@app.callback(
    Output('table_suggested_order_stations', 'data'),
    [Input('table_initial_stations', 'data'),
     Input('table_nb_products', 'data'),
     Input('nb_station_input', 'value'),
     ]
)
def data_table_suggested_order(init_data, table_nb_products, nb_stations):
    if not init_data or not table_nb_products:
        raise PreventUpdate
    # create a list of time needed for each product
    try:
        activities = []
        for row in init_data:
            if '' not in (row['product'], row['activity_block_name'], row['activity_block_duration']):
                row['activity_block_duration'] = float(
                    row['activity_block_duration'])
                activities.append(row)
    except TypeError:
        raise PreventUpdate
    suggested_stations = assign_stations(
        activities, table_nb_products, nb_stations)
    if not suggested_stations:
        raise PreventUpdate
    return suggested_stations


@app.callback(
    Output('graph_suggested_order_stations', 'figure'),
    [Input('table_suggested_order_stations', 'data'),
     Input('input_shift_duration_hour', 'value'),
     Input('input_operator_efficiency', 'value'),
     Input('table_nb_products', 'data')],
    [State('graph_suggested_order_stations', 'figure')]
)
def figure_graph_suggested_order(table_data, input_shift_duration_hour, input_operator_efficiency, table_nb_products, figure):
    if not table_data or not table_nb_products:
        raise PreventUpdate
    df = pd.DataFrame.from_records(table_data)
    df.station_nb = pd.to_numeric(df.station_nb, errors='coerce')
    table_data_names = df.station_nb[~np.isnan(df.station_nb)].unique()
    if not len(table_data_names):
        raise PreventUpdate

    nb_unique_products = len(df['product'].unique())
    station_durations = {}
    for station in table_data_names:
        if not np.isnan(station):
            station_durations[int(station)] = df.loc[df.station_nb ==
                                                     station, 'activity_block_duration'].sum()/nb_unique_products
    figure['data'] = [
        {
            'x': [nb],
            'y': [duration],
            'type': 'bar',
            'name': f'station {nb}'
        } for nb, duration in station_durations.items()
    ]+[
        {
            'x': list(station_durations.keys()),
            'y': [np.mean(list(station_durations.values()))]*len(station_durations),
            'name': 'average station duration'
        }
    ]+[
        {
            'x': list(station_durations.keys()),
            'y': [input_shift_duration_hour*60*input_operator_efficiency/(len(table_data_names)*100)] * len(table_data_names),
            'name': 'takt time'
        }
    ]

    return figure


layout = html.Div(id='pageContent',children=[
    html.H1('Station Balancing page'),
    html.H3('Change takt time by tweaking these parameters: '),
    takt_time_input,
    html.Hr(id="horizontalLine"),
    html.Div(id='instructions',children=['enter the number of stations on the production line']),
    dcc.Input(id='nb_station_input', value=10, type='number',
              min=1, placeholder='number of stations'),
    html.Hr(id="horizontalLine"),
    html.Div(id='instructions',children=['Enter the list of activities for the production']),
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
                   'lineHeight': '30px',
                   'borderWidth': '1px',
                   'borderStyle': 'dashed',
                   'borderRadius': '5px',
                   'textAlign': 'center',
                   'margin': '10px'
               },
               ),
    html.H3('OR'),
    dash_table.DataTable(
        id='table_initial_stations',
        columns=[{'id': name, 'name': name, 'type': type}
                 for name, type in table_colums.items()],
        data=[],
        editable=True,
        row_deletable=True
    ),
    html.Button('Add row', id='add_sation_row'),
    html.Hr(id="horizontalLine"),
    html.Div(id='instructions',children=['Enter the list of product needed to be produced on the same line']),
    dash_table.DataTable(
        id='table_nb_products',
        columns=[{'id': 'product', 'name': 'product', 'type': 'text'},
                 {'id': 'quantity', 'name': 'quantity', 'type': 'numeric', 'editable': True}],
        style_data_conditional=[{
            'if': {'column_id': 'product'},
            'backgroundColor': '#f8f8f8',
        }]
    ),
    html.Hr(id="horizontalLine"),
    html.Div(id='instructions',children=['Suggested stations of for the activity blocks on the production line']),
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
        id='graph_suggested_order_stations',
        figure={
            'layout': {
                'title': 'workload on stations',
                'xaxis': {'title': 'station number'},
                'yaxis': {'title': 'station duration'}
            }
        }
    )
])
