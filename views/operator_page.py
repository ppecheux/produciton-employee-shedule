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

table_input_colums = {"product": "text", "activity_block_name": "text",
                "activity_block_duration": "numeric", "station": "numeric"}

layout = dbc.Container([
    html.H1('Operator scheduling page'),
    html.Div('Enter the list of activities for the production'),
    dcc.Upload(id='upload_station_data',
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
        id='table_initial_stations',
        columns=[{'id': name, 'name': name, 'type': type}
                 for name, type in table_input_colums.items()],
        data=[],
        editable=True,
        row_deletable=True
    ),
    html.Button('Add row', id='add_sation_row'),
    html.Div('Enter the list of product needed to be produced on the same line'),
    dash_table.DataTable(
        id='table_nb_products',
        columns=[{'id': 'product', 'name': 'product', 'type': 'text'},
                {'id': 'quantity', 'name': 'quantity', 'type': 'numeric', 'editable': True}],
        # data=pd.DataFrame({
        #     "product": ["cabine type 1", "cabine type 2", "cabine type 3"],
        #     "quantity": [3, 2, 5]
        # }).to_dict('records'),
        style_data_conditional=[{
            'if': {'column_id': 'product'},
            'backgroundColor': '#f8f8f8',
        }]
    ),
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