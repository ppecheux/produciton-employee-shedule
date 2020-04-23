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
table_input_colums = {"product": "text", "activity_block_name": "text",
                "activity_block_duration": "numeric", "station": "numeric"}

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

layout = dbc.Container([
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
            {'id': 'operator', 'name': 'operator'},
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