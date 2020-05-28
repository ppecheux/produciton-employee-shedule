from app import app
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_table
from views.functions_for_views.functions_for_callbacks import (
    update_table_initial_factory
)

table_input_colums = {"product": "text", "activity_block_name": "text",
                      "activity_block_duration": "text", "station_nb": "numeric"}

layout = html.Div(id='pageContent2', children=[
    html.H1('Save your activities'),
    html.Hr(id="horizontalLine"),
    html.Div(id='instructions', children=[
             'Enter the list of activities for the production']),
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
                   'lineHeight': '30px',
                   'borderWidth': '1px',
                   'borderStyle': 'dashed',
                   'borderRadius': '5px',
                   'textAlign': 'center',
                   'margin-bottom': '50px'
               },
               ),
    html.H3('OR'),

    dash_table.DataTable(
        id='table_initial_operators',
        columns=[{'id': name, 'name': name, 'type': type}
                 for name, type in table_input_colums.items()],
        data=[],
        editable=True,
        row_deletable=True,
        style_cell={
            'backgroundColor': 'white',
            'color': 'black'
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },

    ),
    html.Button('Add row', id='add_operator_row'),
    html.Hr(id="horizontalLine"),
    html.Div(id='instructions', children=[
             'Enter the quantity of product needed to be produced']),
    dash_table.DataTable(
        id='table_nb_products_operator',
        columns=[{'id': 'product', 'name': 'product', 'type': 'text'},
                 {'id': 'quantity', 'name': 'quantity', 'type': 'numeric', 'editable': True}],
        style_cell={
            'backgroundColor': 'white',
            'color': 'black'
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },

    ),

])
