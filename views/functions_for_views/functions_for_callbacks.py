import base64
import io
import pandas as pd
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash import callback_context
from dash.dependencies import Input, Output, State
from app import app
import numpy as np


def update_table_initial_factory(inital_table_id: str, uploader_id: str, add_row_botton: str, table_colums: dict):
    @app.callback([Output(inital_table_id, 'columns'),
                   Output(inital_table_id, 'data')],
                  [Input(uploader_id, 'contents'),
                   Input(add_row_botton, 'n_clicks')],
                  [State(uploader_id, 'filename'),
                   State(inital_table_id, 'data'),
                   State(inital_table_id, 'columns')])
    def update_table_initial_quantity_time(contents, n_clicks, filename, init_data, columns):

        # case we want to add a row
        user_click = callback_context.triggered[0]['prop_id'].split('.')[0]
        if user_click and user_click == add_row_botton:
            init_data.append({c['id']: '' for c in columns})
            return [columns, init_data]
        # case we upload data
        return update_table_from_upload(contents, filename, table_colums)


def update_table_from_upload(contents, filename, table_colums):
    if not filename:
        raise PreventUpdate
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
        raise PreventUpdate

    df.columns = map(str.lower, df.columns)
    columns_to_add = set(df.columns).symmetric_difference(set(table_colums.keys()))
    print(columns_to_add)
    for col in columns_to_add:
        df[col] = ''
    df = df[[column for column in table_colums.keys()]]

    return [[{'name': col.lower(), 'id': col.lower()} for col in df.columns], df.to_dict('records'), ]


def data_table_nb_products_factory(table_nb_products_id: str, inital_table_id: str):
    @app.callback(
        Output(table_nb_products_id, 'data'),
        [Input(inital_table_id, 'data'),
         Input('url', 'href')],
        [State(table_nb_products_id, 'data')]
    )
    def data_table_nb_products(table_initial_stations, href, table_nb_products):
        if not table_initial_stations:
            raise PreventUpdate
        df = pd.DataFrame.from_records(table_initial_stations)
        df['product'] = df['product'].str.strip()
        if table_nb_products:
            df_nb_products = pd.DataFrame.from_records(table_nb_products)
            if set(df['product'].unique()) == set(df_nb_products['product'].unique()):
                raise PreventUpdate
        df_nb_products = pd.DataFrame({
            'product': list(df['product'].unique()),
            'quantity': [1]*len(df['product'].unique())
        })
        return df_nb_products.to_dict('records')


def table_export_format_factory(table_id: str):
    @app.callback(
        Output(table_id, 'export_format'),
        [Input('export_format_toggler', 'value')]
    )
    def table_export_format(toggler_value):
        if toggler_value:
            return 'xlsx'
        return 'csv'

    return table_export_format


def hide_show_factory(id_target: str):
    @app.callback(
        [Output(id_target, 'hidden'), Output(id_target+'_toggler', 'color')],
        [Input(id_target+'_toggler', 'n_clicks')]
    )
    def hide_show(n):
        if n:
            return n%2==0, ('secondary', 'info')[n%2]
        raise PreventUpdate
