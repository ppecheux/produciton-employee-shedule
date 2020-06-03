
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import base64
import dash_daq as daq


external_stylesheets = ['testDash.css']
image_filename = '1200px-DAF_logo.png'
image2_filename = '1200px-Logo_UTC_2018.png'
image3_filename = 'logo-utfpr-png-1.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
encoded_image2 = base64.b64encode(open(image2_filename, 'rb').read())
encoded_image3 = base64.b64encode(open(image3_filename, 'rb').read())

takt_time_input = dbc.Row([
    dbc.Col([
        html.Div(['Duração do turno em horas : ',
                          dcc.Input(id="input_shift_duration_hour", type='number',
                                    placeholder="shift duration: H", value=8, style={'width': 60}),
                          ]),
    ]),
    dbc.Col([
        html.Div(['Eficiência do operator em % : ',
                  dcc.Input(id="input_operator_efficiency", type='number',
                            placeholder="operator efficiency: %", value=91, style={'width': 60}),
                  ]),
    ]),
    dbc.Col([
     html.Button('Change takt time', id='button'),
      ]),
    html.Hr(),
    html.Div(id='output-container-button',
             children='')
])
NavBar = html.Div(
    id='header',
    children=[
        # List displayed horizontaly
        html.Ul(
            id='navigation',
            children=[
                html.Img(
                    src='data:image/png;base64,{}'.format(encoded_image.decode())),
                html.Li(
                    children=[html.A('Tutorial', id='tutorial_page', href='/tutorials')]),
                html.Li(
                    children=[html.A('Estações', id='station_mix', href='/station')]),
                html.Li(
                    children=[html.A('Operadores', id='operators_mix', href='/operator')]),
                html.Li(children=[html.A('Mix de Produção',
                                         id='Production_mix', href='/mix')]),
                html.Li(children=[html.A('actividades',
                                         id='actividades', href='/actividades')]),
            ]),
    ])
Footer = html.Div(
    id='footer',
    children=[
        html.Ul(
            id='bottom_page',
            children=[
                html.Li(
                    'Software desenvolvido pela parceria :'),
                html.Li(
                    children=[
                        html.Img(
                            src='data:image/png;base64,{}'.format(encoded_image2.decode())),
                    ]),
                html.Li(
                    children=[
                        html.Img(style={
                            'width': '12%'}, src='data:image/png;base64,{}'.format(encoded_image3.decode())),
                    ]),
            ]),
    ])

export_format_toggler = dbc.Row([
    dbc.Col(
        html.Div("Formato para exportar"), width=4, lg=2
    ),
    dbc.Col(
        html.Div("csv"), width=1
    ),
    dbc.Col(
        daq.ToggleSwitch(id='export_format_toggler'), width=3, lg=2
    ),
    dbc.Col(
        html.Div("xlsx"), width=1
    )
])

def hidde_show_toggler(id_target: str):
    return daq.ToggleSwitch(
        id = id_target+'_toggler',
        label='show',
        labelPosition='left',
        value=True
    )
