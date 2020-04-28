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

from algos.employee_tasks import assign_employee
table_input_colums = {"product": "text", "activity_block_name": "text",
                "activity_block_duration": "numeric", "station_nb": "numeric"}

@app.callback([Output('table_initial_operators', 'columns'),
               Output('table_initial_operators', 'data')],
              [Input('upload_operator_data', 'contents'),
               Input('add_operator_row', 'n_clicks')],
              [State('upload_operator_data', 'filename'),
               State('table_initial_operators', 'data'),
               State('table_initial_operators', 'columns')])
def update_table_initial_quantity_time(contents, n_clicks, filename, init_data, columns):

    # case we want to add a row
    user_click = callback_context.triggered[0]['prop_id'].split('.')[0]
    if user_click and user_click == 'add_operator_row':
        init_data.append({c['id']: '' for c in columns})
        return [columns, init_data]
    # case we upload data
    return update_table_from_upload(contents, filename, table_input_colums)

@app.callback(
    Output('table_nb_products_operator', 'data'),
    [Input('table_initial_operators', 'data')],
    [State('table_nb_products_operator', 'data')]
)
def data_table_nb_products_operator(table_initial_operators, table_nb_products_operator):
    return data_table_nb_products(table_initial_operators, table_nb_products_operator)


@app.callback(
    Output('table_suggested_operator', 'data'),
    [Input('table_initial_operators', 'data'),
     Input('table_nb_products_operator', 'data'),
     Input('input_shift_duration_hour', 'value'),
     Input('input_operator_efficiency', 'value')]
)
def data_table_suggested_order(init_data, table_nb_products, input_shift_duration_hour, input_operator_efficiency):
    if not init_data or not table_nb_products:
        raise PreventUpdate
    # create a list of time needed for each product
    try:
        activities = []
        for row in init_data:
            if '' not in (row['product'], row['activity_block_name'], row['activity_block_duration'], row['station_nb']):
                row['activity_block_duration'] = float(
                    row['activity_block_duration'])
                row['station_nb'] = int(row['station_nb'])
                activities.append(row)
    except TypeError:
        raise PreventUpdate
    print(pd.DataFrame.from_records(activities))
    suggested_operators = assign_employee(
        activities, table_nb_products, int(input_shift_duration_hour), float(input_operator_efficiency))
    print(pd.DataFrame.from_dict(suggested_operators))
    if not suggested_operators:
        raise PreventUpdate
    return suggested_operators

@app.callback(
    Output('graph_suggested_operators', 'figure'),
    [Input('table_suggested_operator', 'data'),
     Input('input_shift_duration_hour', 'value'),
     Input('input_operator_efficiency', 'value'),
     Input('table_nb_products_operator', 'data')],
    [State('graph_suggested_operators', 'figure')]
)
def figure_graph_suggested_order(table_data, input_shift_duration_hour, input_operator_efficiency, table_nb_products, figure):
    if not table_data or not table_nb_products:
        raise PreventUpdate
    df = pd.DataFrame.from_records(table_data)
    df.station_nb = pd.to_numeric(df.operator_nb, errors='coerce')
    table_data_names = df.operator_nb[~np.isnan(df.station_nb)].unique()
    if not len(table_data_names):
        raise PreventUpdate

    nb_unique_products = len(df['product'].unique())
    station_durations = {}
    for operator in table_data_names:
        if not np.isnan(operator):
            station_durations[int(operator)] = df.loc[df.operator_nb ==
                                                     operator, 'activity_block_duration'].sum()/nb_unique_products
    figure['data'] = [
        {
            'x': [nb],
            'y': [duration],
            'type': 'bar',
            'name': f'operator {nb}'
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
    html.H1('Operator scheduling page'),
    takt_time_input,
    html.Div('Enter the list of activities for the production'),
    dcc.Upload(id='upload_operator_data',
               children=html.Div(
                   [
                       'Drag and Drop or ',
                       html.A('Select File'),
                       f' (csv or xls) \n must have {table_input_colums.keys()} columns'
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
        id='table_initial_operators',
        columns=[{'id': name, 'name': name, 'type': type}
                 for name, type in table_input_colums.items()],
        data=[],
        editable=True,
        row_deletable=True
    ),
    html.Button('Add row', id='add_operator_row'),
    html.Div('Enter the quantity of product needed to be produced'),
    dash_table.DataTable(
        id='table_nb_products_operator',
        columns=[{'id': 'product', 'name': 'product', 'type': 'text'},
                {'id': 'quantity', 'name': 'quantity', 'type': 'numeric', 'editable': True}],
        style_data_conditional=[{
            'if': {'column_id': 'product'},
            'backgroundColor': '#f8f8f8',
        }]
    ),
    html.H3('Suggested activities for the operators'),
    dash_table.DataTable(
        id='table_suggested_operator',
        columns=[
            {'id': 'product', 'name': 'product'},
            {'id': 'activity_block_name', 'name': 'activity_block_name'},
            {'id': 'activity_block_duration', 'name': 'activity_block_duration'},
            {'id': 'station_nb', 'name': 'station'},
            {'id': 'operator_nb', 'name': 'operator'},
        ]
    ),
    dcc.Graph(
        id='graph_suggested_operators',
        figure={
            'layout': {
                'title': 'workload on operators',
                'xaxis': {'title': 'operator number'},
                'yaxis': {'title': 'operator duration'}
            }
        }
    )
])