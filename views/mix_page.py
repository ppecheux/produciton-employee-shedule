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
import base64
from views.functions_for_views.functions_for_callbacks import update_table_from_upload, table_export_format_factory
from views.functions_for_views.input_components import takt_time_input, export_format_toggler

from algos.production_mix import merge_mix
external_stylesheets = ['testDash.css']
image_filename = '1200px-DAF_logo.png'
image2_filename = '1200px-Logo_UTC_2018.png'
image3_filename = 'logo-utfpr-png-1.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
encoded_image2 = base64.b64encode(open(image2_filename, 'rb').read())
encoded_image3 = base64.b64encode(open(image3_filename, 'rb').read())

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
    user_click = callback_context.triggered[0]['prop_id'].split('.')[0]
    if user_click and user_click == 'add_button':
        init_data.append({c['id']: '' for c in columns})
        return [columns, init_data]
    # case we upload data
    return update_table_from_upload(contents, filename, table_colums)


table_export_format_factory('table_suggested_order')


@app.callback(
    Output('table_suggested_order', 'data'),
    [Input('table_initial_quantity_time', 'data')]
)
def data_table_suggested_order(init_data):
    if not init_data:
        raise PreventUpdate

    # create a list of time needed for each product
    df_activities = pd.DataFrame.from_records(init_data)
    df_activities.replace('', np.nan, inplace=True)
    df_activities.dropna(inplace=True)
    df_activities.name.str.strip()

    try:
        df_activities = df_activities.astype({"quantity": int})
    except ValueError:
        raise PreventUpdate

    try:
        df_activities = df_activities.astype({"time": float})
    except ValueError:
        try:
            df_activities['time'] = pd.to_timedelta(df_activities.time).dt.total_seconds() / 60
        except ValueError:
            print("echec de conversion des durées")
            raise PreventUpdate

    activities = df_activities.to_records()
    times = []
    for row in activities:
        times.extend([row['time']] * row['quantity'])
    mixed_times = merge_mix(times)

    # create data for the suggested order table
    suggested_data = []
    cumulated_time = 0
    for time in mixed_times:
        cumulated_time += time
        for row in activities:
            if row['quantity'] > 0 and row['time'] == time:
                suggested_data.append(
                    {
                        'name': row['name'],
                        'time': time,
                        'cumulated_time': cumulated_time
                    }
                )
                row['quantity'] = int(row['quantity']) - 1

    return suggested_data


@app.callback(
    Output('graph_suggested_order', 'figure'),
    [Input('table_suggested_order', 'data'),
     Input('input_shift_duration_hour', 'value'),
     Input('input_operator_efficiency', 'value')],
    [State('graph_suggested_order', 'figure')]
)
def figure_graph_suggested_order(table_data, input_shift_duration_hour, input_operator_efficiency, figure):
    if not table_data:
        raise PreventUpdate

    table_data_names = [row['name'] for row in table_data]
    table_data_times = [float(row['time']) for row in table_data]
    figure['data'] = [
        {
            'x': [indice for indice, v in enumerate(table_data_names) if v == name],
            'y': [table_data_times[table_data_names.index(name)]]*table_data_names.count(name),
            'type': 'bar',
            'name': name
        } for name in set(table_data_names)
    ]+[
        {
            'x': list(range(len(table_data_names))),
            'y': [np.mean(table_data_times)]*len(table_data_names),
            'name': 'average production time'}
    ]+[
        {
            'x': list(range(len(table_data_names))),
            'y': [input_shift_duration_hour*60*input_operator_efficiency/(len(table_data_names)*100)] * len(table_data_names),
            'name': 'takt time'
        }
    ]

    return figure


layout = html.Div(id='pageContent2', children=[
    html.H1("Página do Mix de Produção"),
    html.Br(),
    html.H3('Altere o takt time configurando estes parâmetros '),
    takt_time_input,
    html.Hr(id="horizontalLine"),
    html.Div(id='instructions', children=[
             'Lista de productos a serem produzidos']),
    dcc.Upload(
        id='upload_mix_data',
        children=html.Div(
            [
                'Arraste e solte, ou selecione un arquivo ',
                html.A('Select File'),
                ' (csv or xls) \n deve ter as colunas modelo, tempo e quantitade'
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
    html.Button('Adicionar linha', id='add_button'),
    html.Hr(id="horizontalLine"),
    html.Div(id='instructions', children=[
             'Ordem sugerida dos productos na linha de produção']),
    export_format_toggler,
    html.H1(''),
    dash_table.DataTable(
        id='table_suggested_order',
        columns=[
            {'id': 'name', 'name': 'modelo'},
            {'id': 'time', 'name': 'tempo'},
            {'id': 'cumulated_time', 'name': 'tempo acumulado'}
        ],
        sort_action="native",
        export_format='csv',
        export_headers='names',
        style_cell={
        'backgroundColor': 'white',
        'color': 'black'   
    },
        style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    },
    ),
    dcc.Graph(
        id='graph_suggested_order',
        figure={
            'layout': {
                'title': 'Vizualização da ordem de produção',
                'xaxis': {'title': 'Ordem da linha de produção'},
                'yaxis': {'title': 'Tempo de produção'}
            }
        },
        config={
            'displaylogo': False
        }
    )
])
