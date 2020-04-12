import base64
import io
import pandas as pd
import dash_html_components as html

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