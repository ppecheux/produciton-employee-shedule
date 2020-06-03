import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from app import app, server
from views.functions_for_views.input_components import NavBar
from views.functions_for_views.input_components import Footer
from views import error, mix_page, station_page, operator_page, homepage, tutorials, activity_table
from datetime import datetime as dt
import sys

dashboard_pages = {'/mix': mix_page,
                   '/station': station_page, '/operator': operator_page, '/tutorials':tutorials}
app.layout = html.Div([
    dcc.Location(id='url'),
    html.Div(id='homepage', children=[
        NavBar
    ]),
    html.Div(id='pageContent'),

    Footer
])

@app.callback(Output('pageContent', 'children'),
              [Input('url', 'pathname')])
def displayPage(pathname):
    layout = None
    for pathname_dashboard, file in dashboard_pages.items():
        if pathname == pathname_dashboard and file:
            layout = file.layout

    if pathname == '/':
        layout = homepage.layout

    elif pathname == '/actividades':
        layout = activity_table.layout

    elif not layout:
        layout = error.layout
        print(f'path error {pathname}')
    return layout


@app.callback(
    Output('navBar', 'children'),
    [Input('pageContent', 'children')])
def navBar_children(input1):

    DAF_LOGO = "https://upload.wikimedia.org/wikipedia/commons/1/12/DAF_logo.svg"
    DashboardNavItems = [
        html.A(dbc.Col(html.Img(src=DAF_LOGO, height="30px")),
               href="https://daf.com"),
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink(href.replace('/', '').title().replace('_', ' ').capitalize(),
                                        href=href))
                for href in dashboard_pages.keys()
            ],
            justified=True)
    ]
    return DashboardNavItems

@app.callback(
    Output(component_id='output-container-button', component_property='children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input_shift_duration_hour', 'value'),
    dash.dependencies.State('input_operator_efficiency', 'value')],
)
def update_output_div(n_clicks,input_shift_duration_hour_value,input_operator_efficiency_value):
    return 'Takt time will be calculated with the number of trucks to produce, but the vailable time per employee per day in minutes is now {}'.format(input_shift_duration_hour_value*60*input_operator_efficiency_value/100)


if __name__ == '__main__':
    app.run_server(debug=True)
