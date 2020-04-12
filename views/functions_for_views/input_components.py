
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

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
