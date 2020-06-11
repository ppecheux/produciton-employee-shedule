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
        dbc.Card(['⏳Duração do turno em horas : ',
                          dcc.Input(id="input_shift_duration_hour", type='number',
                                    placeholder="shift duration: H", value=8, style={'width': '100%'}),
                          ]),
    ]),
    dbc.Col([
        dbc.Card(['👨🏼‍🏭 Eficiência do operator em % : ',
                  dcc.Input(id="input_operator_efficiency", type='number',
                            placeholder="operator efficiency: %", value=91, style={'width': '100%'}),
                  ]),
    ]),
    dbc.Col([
        dbc.Button('Alterar Takt Time', id='button'),
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
                    children=[html.A('Tutorial', id='tutorial_page', href='/tutorial')]),
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

NavBar = dbc.Navbar(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Img(
                        src='data:image/png;base64,{}'.format(encoded_image.decode())),
                ),
                dbc.Col(
                    dbc.NavItem(dbc.NavLink("Tutorial", href="/tutorials")),
                ),
                dbc.Col(
                    dbc.NavItem(dbc.NavLink(
                        'Estações', id='station_mix', href='/station')),
                ),
                dbc.Col(
                    dbc.NavItem(dbc.NavLink(
                        'Operadores', id='operators_mix', href='/operator')),
                ),
                dbc.Col(
                    dbc.NavItem(dbc.NavLink('Mix de Produção',
                                            id='Production_mix', href='/mix')),
                ),
                dbc.Col(
                    dbc.NavItem(dbc.NavLink('Actividades',
                                            id='actividades', href='/actividades')),
                ),
            ]
        )
    ]
)

NavBar = dbc.NavbarSimple(
    [
        dbc.NavbarBrand(
        html.Img(
            src='data:image/png;base64,{}'.format(encoded_image.decode())),
        ),
        dbc.NavItem(dbc.NavLink("Tutorial", href="/tutorials")),
        dbc.NavItem(dbc.NavLink(
            'Estações', id='station_mix', href='/station')),
        dbc.NavItem(dbc.NavLink(
            'Operadores', id='operators_mix', href='/operator')),
        dbc.NavItem(dbc.NavLink('Mix de Produção',
                                id='Production_mix', href='/mix')),
        dbc.NavItem(dbc.NavLink('Atividades',
                                id='Actividades', href='/actividades')),

    ]
)

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
    return dbc.Button(
        id=id_target+'_toggler',
        children='mostrar entrada de atividades',
    )