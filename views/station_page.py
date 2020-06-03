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
    update_table_initial_factory,
    hide_show_factory)
from views.functions_for_views.input_components import (
    takt_time_input,
    export_format_toggler,
    hidde_show_toggler)
from algos.stations import assign_stations
from config import engine

table_colums = {"product": "text", "activity_block_name": "text",
                "activity_block_duration": "text", "min_sequence_rank": "text", "max_sequence_rank": "text"}

update_table_initial_factory(
    'table_initial_stations', 'upload_station_data', 'add_sation_row', table_colums)

data_table_nb_products_factory('table_nb_products', 'table_initial_stations')

table_export_format_factory('table_suggested_order_stations')


def get_init_data_from_db():
    df = pd.read_sql_table(table_name="activity", con=engine)
    df.loc[~pd.isna(df.station_nb)] = df[~pd.isna(
        df.station_nb)].astype({"station_nb": int})
    df['activity_block_duration'] = pd.to_timedelta(
        df['activity_block_duration']).astype({"activity_block_duration": str})
    records = df[[c for c in table_colums]].to_dict('rows')
    return records


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
    df_activities = pd.DataFrame.from_records(init_data)
    df_activities[['product', 'activity_block_name',
                   'activity_block_duration']].replace('', np.nan, inplace=True)
    df_activities['product'] = df_activities['product'].str.strip()
    df_activities['activity_block_name'] = df_activities['activity_block_name'].str.strip()
    df_activities.dropna(inplace=True, subset=[
                         'product', 'activity_block_name', 'activity_block_duration'])
    df_activities['activity_block_name'] = df_activities['activity_block_name'].str.strip()
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
    df_activities = df_activities.astype(
        {"min_sequence_rank": str, "max_sequence_rank": str})
    activities = df_activities.to_records()
    suggested_stations = assign_stations(
        activities, table_nb_products, nb_stations)
    if not suggested_stations:
        raise PreventUpdate
    df_suggested = pd.DataFrame.from_dict(suggested_stations)
    if isinstance(df_suggested['activity_block_duration'].iloc[0], pd.Timedelta):
        df_suggested['activity_block_duration'] /= pd.Timedelta(minutes=1)
    suggested_stations = df_suggested.to_dict('rows')
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


layout = html.Div(id='pageContent2', children=[
    html.H1('Página do Balanceamento de Estações'),
    html.H3('Altere o takt time configurando estes parâmetros'),
    takt_time_input,
    html.Hr(id="horizontalLine"),
    dbc.Card([
        'Forneça o número de estações na linha de produção',
        dcc.Input(id='nb_station_input', value=10, type='number',
                  min=1, placeholder='number of stations'),
    ],
    style={"width": "30%", }),
    html.Hr(id="horizontalLine"),
    hidde_show_toggler('input_data_table_div'),
    html.Div(id='input_data_table_div',
             children=[
                 'Forneça a lista das atividades da produção',
                 dcc.Upload(id='upload_station_data',
                            children=dbc.Card(
                                [
                                    '📁',
                                    f' (csv or xls) \n  Deve conter o cabeçalho : {", ".join((k for k in table_colums))} '
                                ]
                            ),
                            ),
                 html.H3('OU'),
                 dash_table.DataTable(
                     id='table_initial_stations',
                     columns=[{'id': name, 'name': name, 'type': type}
                              for name, type in table_colums.items()],
                     data=get_init_data_from_db(),
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
                 html.Button('adicionar linha', id='add_sation_row'),
             ],
             hidden=True),
    html.Hr(id="horizontalLine"),
    html.Div(id='instructions', children=[
             'Forneça a lista de modelos a ser produzida na linha de produção']),
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
    html.Div(id='instructions', children=[
             'Estações sugeridas para os blocos de atividade da linha de produção']),

    export_format_toggler,
    html.H3(''),

    dash_table.DataTable(
        id='table_suggested_order_stations',
        columns=[
            {'id': 'product', 'name': 'product'},
            {'id': 'activity_block_name', 'name': 'activity_block_name'},
            {'id': 'activity_block_duration', 'name': 'activity_block_duration'},
            {'id': 'station_nb', 'name': 'station_nb'}
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
        id='graph_suggested_order_stations',
        figure={
            'layout': {
                'title': 'workload on stations',
                'xaxis': {'title': 'número da estação'},
                'yaxis': {'title': 'duração da estação'}
            }
        },
        config={
            'displaylogo': False
        }
    )
])
