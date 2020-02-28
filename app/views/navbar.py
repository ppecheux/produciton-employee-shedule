import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
from app import app, server
from flask_login import current_user
from views import mix_page


dashboard_pages = {'/mix_page': mix_page}

navBar = dbc.NavbarSimple(id='navBar',
                          children=[],
                          sticky='top',
                          dark=False,
                          fluid=True,  # for simple
                          expand='xl'
                          # className='navbar navbar-expand-lg navbar-dark bg-primary',
                          )

@app.callback(
    Output('navBar', 'children'),
    [Input('pageContent', 'children')])
def navBar_children(input1):
    DashboardNavItems = [
        dbc.NavItem(dbc.NavLink(href.replace('/', '').title().replace('-', ' '),
                                href=href))
        for href in dashboard_pages.keys()
    ]
    if current_user.is_authenticated:
        if current_user.admin == 1:
            navBarContents = DashboardNavItems + [
                dbc.DropdownMenu(
                    nav=True,
                    in_navbar=True,
                    label=current_user.username,
                    children=[
                        dbc.DropdownMenuItem('Profile', href='/profile'),
                        dbc.DropdownMenuItem('Admin', href='/admin'),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem('Logout', href='/logout'),
                    ],
                ),
            ]
            return navBarContents

        else:
            navBarContents = DashboardNavItems + [
                dbc.DropdownMenu(
                    nav=True,
                    in_navbar=True,
                    label=current_user.username,
                    children=[
                        dbc.DropdownMenuItem('Profile', href='/profile'),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem('Logout', href='/logout'),
                    ],
                ),
            ]
            return navBarContents

    else:
        return ''
