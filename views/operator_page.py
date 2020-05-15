import datetime
import numpy as np
import pandas as pd
from app import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_table
from views.functions_for_views.functions_for_callbacks import (
    update_table_from_upload,
    data_table_nb_products_factory,
    table_export_format_factory,
    update_table_initial_factory)
from views.functions_for_views.input_components import takt_time_input, export_format_toggler

from algos.employee_tasks import assign_employee
table_input_colums = {"product": "text", "activity_block_name": "text",
                      "activity_block_duration": "text", "station_nb": "numeric"}

update_table_initial_factory('table_initial_operators', 'upload_operator_data', 'add_operator_row', table_input_colums)

table_export_format_factory('table_suggested_operator')

@app.callback(
    Output('table_suggested_operator', 'data'),
    [Input('table_initial_operators', 'data'),
     Input('table_nb_products_operator', 'data'),
     Input('input_shift_duration_hour', 'value'),
     Input('input_operator_efficiency', 'value')],
)
def data_table_suggested_order(init_data, table_nb_products, input_shift_duration_hour, input_operator_efficiency):
    print('in suggestion')
    if not init_data or not table_nb_products:
        raise PreventUpdate
    # create a list of time needed for each product
    df_activities = pd.DataFrame.from_records(init_data)
    df_activities['product'] = df_activities['product'].str.strip()
    df_activities['activity_block_name'] = df_activities['activity_block_name'].str.strip()
    df_activities.replace('', np.nan, inplace=True)
    df_activities.dropna(inplace=True)
    try:
        df_activities = df_activities.astype({"station_nb": int})
    except ValueError:
        print('the stations are not int')
        raise PreventUpdate

    try:
        df_activities = df_activities.astype(
            {"activity_block_duration": float})
    except ValueError:
        try:
            df_activities['activity_block_duration'] = pd.to_timedelta(
                df_activities.activity_block_duration)
        except ValueError:
            print("echec de conversion des durées")
            raise PreventUpdate

    activities = df_activities.to_records()
    suggested_operators = assign_employee(
        activities, table_nb_products, int(input_shift_duration_hour), float(input_operator_efficiency))
    df_suggested = pd.DataFrame.from_dict(suggested_operators)
    if not suggested_operators:
        raise PreventUpdate
    if isinstance(df_suggested['activity_block_duration'].iloc[0], pd.Timedelta):
        df_suggested['activity_block_duration'] /= pd.Timedelta(minutes=1)
    suggested_operators = df_suggested.to_dict('rows')
    return suggested_operators


data_table_nb_products_factory(
    'table_nb_products_operator', 'table_initial_operators')


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
    df = df.merge(pd.DataFrame.from_records(table_nb_products),
                  how="left",
                  on="product")
    df['total_duration_activity'] = df['quantity']*df['activity_block_duration']
    df.station_nb = pd.to_numeric(df.operator_nb, errors='coerce')
    table_data_names = df.operator_nb[~np.isnan(df.station_nb)].unique()
    if not len(table_data_names):
        raise PreventUpdate

    nb_unique_products = len(df['product'].unique())
    operator_duration = {}
    for operator in table_data_names:
        if not np.isnan(operator):
            operator_duration[int(operator)] = df.loc[df.operator_nb ==
                                                      operator, 'total_duration_activity'].sum()
    figure['data'] = [
        {
            'x': [nb],
            'y': [duration],
            'type': 'bar',
            'name': f'operator {nb}'
        } for nb, duration in operator_duration.items()
    ]+[
        {
            'x': list(operator_duration.keys()),
            'y': [np.mean(list(operator_duration.values()))]*len(operator_duration),
            'name': 'average operator work duration'
        }
    ]+[
        {
            'x': list(operator_duration.keys()),
            'y': [input_shift_duration_hour*60*input_operator_efficiency/100] * len(table_data_names),
            'name': 'target work duration'
        }
    ]

    return figure


layout = html.Div(id='pageContent2', children=[
    html.H1('Operator scheduling page'),
    html.H3('Change takt time by tweaking these parameters: '),
    takt_time_input,
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
        row_deletable=True
    ),
    html.Button('Add row', id='add_operator_row'),
    html.Hr(id="horizontalLine"),
    html.Div(id='instructions', children=[
             'Enter the quantity of product needed to be produced']),
    dash_table.DataTable(
        id='table_nb_products_operator',
        columns=[{'id': 'product', 'name': 'product', 'type': 'text'},
                 {'id': 'quantity', 'name': 'quantity', 'type': 'numeric', 'editable': True}],
        style_data_conditional=[{
            'if': {'column_id': 'product'},
            'backgroundColor': '#f8f8f8',
        }]
    ),
    html.Hr(id="horizontalLine"),
    html.H3('Suggested activities for the operators'),
    export_format_toggler,
    dash_table.DataTable(
        id='table_suggested_operator',
        columns=[
            {'id': 'product', 'name': 'product'},
            {'id': 'activity_block_name', 'name': 'activity_block_name'},
            {'id': 'activity_block_duration', 'name': 'activity_block_duration'},
            {'id': 'station_nb', 'name': 'station'},
            {'id': 'operator_nb', 'name': 'operator'},
        ],
        sort_action="native",
        export_format='csv',
        export_headers='names'
    ),
    dcc.Graph(
        id='graph_suggested_operators',
        figure={
            'layout': {
                'title': 'total work duration in a day',
                'xaxis': {'title': 'operator number'},
                'yaxis': {'title': 'operator duration in minutes'}
            }
        },
        config={
            'displaylogo': False
        }
    )
])
