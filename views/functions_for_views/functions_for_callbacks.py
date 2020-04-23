import base64
import io
import pandas as pd
import dash_html_components as html
from dash.exceptions import PreventUpdate


def update_table_from_upload(contents, filename, table_colums):

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

    df.columns = map(str.lower, df.columns)
    df = df[[column for column in table_colums.keys()]]

    return [[{'name': col.lower(), 'id': col.lower()} for col in df.columns], df.to_dict('records'), ]

def data_table_nb_products(table_initial_stations, table_nb_products):
    if not table_initial_stations:
        raise PreventUpdate
    df = pd.DataFrame.from_records(table_initial_stations)
    if table_nb_products:
        df_nb_products = pd.DataFrame.from_records(table_nb_products)
        if set(df['product'].unique()) == set(df_nb_products['product'].unique()):
            raise PreventUpdate
    df_nb_products = pd.DataFrame({
        'product': list(df['product'].unique()),
        'quantity': [1]*len(df['product'].unique())
    })
    return df_nb_products.to_dict('records')