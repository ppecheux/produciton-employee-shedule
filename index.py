# import for requirements

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from app import app, server
from flask_login import logout_user, current_user

from views import login, error, profile, user_admin, navbar, mix_page
from views.navbar import navBar, dashboard_pages
from datetime import datetime as dt
import sys


app.layout = html.Div([
    dcc.Location(id='url'),
    dcc.Store(id='url_asked_at_login', storage_type='session'),
    html.Div([
        navBar,
        html.Div(id='pageContent')
    ])
], id='table-wrapper')


@app.callback(Output('pageContent', 'children'),
              [Input('url', 'pathname')])
def displayPage(pathname):
    layout = None

    for pathname_dashboard, file in dashboard_pages.items():
        if pathname == pathname_dashboard and file:
            if current_user.is_authenticated:
                layout = file.layout
            else:
                layout = login.layout

    if pathname == '/':
        if current_user.is_authenticated:
            layout = profile.layout
        else:
            layout = login.layout

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

    elif not layout:
        layout = error.layout

    return layout


if __name__ == '__main__':
    app.run_server(debug=True)
