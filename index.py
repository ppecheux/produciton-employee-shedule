import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from app import app, server
from flask_login import logout_user, current_user
from views.functions_for_views.input_components import NavBar
from views.functions_for_views.input_components import Footer
from views import login, error, profile, user_admin, mix_page, success_login
from views import mix_page, station_page, operator_page, homepage

from datetime import datetime as dt
import sys

dashboard_pages = {'/mix': mix_page,
                   '/station': station_page, '/operator': operator_page}
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
    print(f'path_name {pathname}')
    for pathname_dashboard, file in dashboard_pages.items():
        if pathname == pathname_dashboard and file:
            layout = file.layout
            # if current_user.is_authenticated:
            # else:
            #     layout = login.layout

    if pathname == '/':
        if current_user.is_authenticated:
            layout = profile.layout
        else:
            layout = homepage.layout

    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
        layout = login.layout

    elif pathname == '/profile':
        if current_user.is_authenticated:
            layout = profile.layout
        else:
            layout = login.layout

    elif pathname == '/admin':
        if current_user.is_authenticated:
            if current_user.admin:
                layout = user_admin.layout
            else:
                layout = error.layout
        else:
            layout = login.layout

    elif pathname == '/success_login':
        layout = success_login.layout

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


if __name__ == '__main__':
    app.run_server(debug=True)
