import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_table

table_colums = {"name": "text", "time": "number", "quantity": "number"}

layout = dbc.Container([
    dbc.Row([dbc.Col(dcc.Input(f'input_{name}', type=type, placeholder=name)) for name, type in table_colums.items()] + [
        dbc.Col(html.Button('Add', id='add_button'))
    ]),
    dash_table.DataTable(
        id='table_initial_quantity_time',
        columns=[{'id': name, 'name': name} for name in table_colums.keys()],
        editable=True
    )
])