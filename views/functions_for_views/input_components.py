
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import base64

external_stylesheets = ['testDash.css']
image_filename = '1200px-DAF_logo.png' 
image2_filename = '1200px-Logo_UTC_2018.png'
image3_filename = 'logo-utfpr-png-1.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
encoded_image2 = base64.b64encode(open(image2_filename, 'rb').read())
encoded_image3 = base64.b64encode(open(image3_filename, 'rb').read())

takt_time_input = dbc.Row([
    dbc.Col([
        html.Div(['shift duration in Hour : ',
                          dcc.Input(id="input_shift_duration_hour", type='number',
                                    placeholder="shift duration: H", value=8, style={'width': 60}),
                          ]),
    ]),
    dbc.Col([
        html.Div(['operator efficiency in % : ',
                  dcc.Input(id="input_operator_efficiency", type='number',
                            placeholder="operator efficiency: %", value=91, style={'width': 60}),
                  ]),
    ]),
])
NavBar=html.Div(id='header',children=[
    #List displayed horizontaly
    html.Ul(id='navigation',children=[
        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode())),
        html.Li(children=[ html.A('Tutorial',id='tutorial_page',href='/tutorial')]),
        html.Li(children=[html.A('Estações', id='station_mix',href='/station')]),
        html.Li(children=[ html.A('Operadores', id='operators_mix',href='/operator_page')]),
        html.Li(children=[ html.A('Mix de Produçaõ', id='Production_mix',href='/mix')]),
        html.Li(children=[ html.A('Entrar',style={'border-radius':'30%','border':'2px solid red'}, id='entry')]),
    ]),
    ])
Footer=html.Div(id='footer',children=[
        html.Ul(id='bottom_page',children=[
            html.Li('Software desenvolvido pela parceria :'),
            html.Li(children=[
                html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode())),
                ]),
            html.Li(children=[
                html.Img(style={'width':'12%'},src='data:image/png;base64,{}'.format(encoded_image3.decode())),
                ]),         
        ]),
    ])
