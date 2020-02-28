import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_table
from app import app

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

layout = dbc.Container([
    html.H1('List of product needed to be produce'),
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
    )
])

