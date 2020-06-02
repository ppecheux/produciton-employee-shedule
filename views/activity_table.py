from app import app
import dash_html_components as html
import dash_core_components as dcc
from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import numpy as np
from views.functions_for_views.functions_for_callbacks import (
    update_table_initial_factory
)
from input_base_managent import delete_all_activies, add_Activity
from statsmodels.compat import cStringIO
from config import engine
from views.station_page import table_colums
from views.operator_page import table_input_colums

table_input_colums.update(table_colums)


@app.callback(Output('save', 'children'),
              [Input('save', 'n_clicks'),
               Input('table_initial_operators', 'data')],
              )
def save_activity_data(n_click, data):
    if not n_click or not data:
        raise PreventUpdate
    saved = ''
    user_click = callback_context.triggered[0]['prop_id'].split('.')[0]
    if user_click and user_click == 'save':
        saved = ' ✔️'
        # delete_all_activies()
        df = pd.DataFrame.from_records(data)
        df['product'] = df['product'].str.strip()
        df['activity_block_name'] = df['activity_block_name'].str.strip()
        df.replace('', np.nan, inplace=True)
        df.dropna(
            inplace=True,
            subset=["product", "activity_block_name",
                    "activity_block_duration"]
        )
        try:
            df.loc[~pd.isna(df.station_nb)] = df[~pd.isna(
                df.station_nb)].astype({"station_nb": int})
        except ValueError:
            print('the stations are not int')
            raise PreventUpdate
        try:
            pd.to_numeric(df['activity_block_duration'])
            df['activity_block_duration'] = df['activity_block_duration'] + ' min'
        except ValueError:
            pass

        try:
            df['activity_block_duration'] = pd.to_timedelta(
                df.activity_block_duration)
        except ValueError:
            print("echec de conversion des durées")
            raise PreventUpdate

        print(df)
        df.to_sql('activity', con=engine, if_exists='replace')

    return "save" + saved


layout = html.Div(id='pageContent2', children=[
    html.H1('Save your activities'),
    html.Hr(id="horizontalLine"),
    html.Div(id='instructions', children=[
             'Enter the list of activities for the production']),
    dcc.Upload(id='upload_operator_data',
               children=dbc.Card(
                   [
                       '📁',
                       f' (csv or xls) \n Deve conter o cabeçalho : {", ".join((k for k in table_input_colums))} '
                   ]
               ),
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
    html.Button('Save', id='save'),

])
