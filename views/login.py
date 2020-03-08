import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app, User
from flask_login import login_user
from werkzeug.security import check_password_hash


layout = dbc.Container([
    html.Br(),
    dbc.Container([
        html.Div([
            dbc.Container(
                html.Img(
                    src='/assets/dash-logo-stripe.svg',
                    className='center'
                ),
            ),
            dbc.Container(id='loginType', children=[
                dcc.Input(
                    placeholder='Enter your username',
                    type='text',
                    id='usernameBox',
                    className='form-control',
                    n_submit=0,
                ),
                html.Br(),
                dcc.Input(
                    placeholder='Enter your password',
                    type='password',
                    id='passwordBox',
                    className='form-control',
                    n_submit=0,
                ),
                html.Br(),
                html.Button(
                    children='Login',
                    n_clicks=0,
                    type='submit',
                    id='loginButton',
                    className='btn btn-primary btn-lg'
                ),
                html.Br(),
            ], className='form-group'),
        ]),
    ], className='jumbotron')
])


@app.callback([Output('url', 'pathname'), Output('success_login_link', 'children')],
              [Input('loginButton', 'n_clicks')],
               [State('usernameBox', 'n_submit'),
               State('passwordBox', 'n_submit'),
              State('usernameBox', 'value'),
               State('passwordBox', 'value'),
               State('url', 'pathname')])
def sucess(n_clicks, usernameSubmit, passwordSubmit, username, password, pathname):
    if (n_clicks > 0) or (usernameSubmit > 0) or (passwordSubmit) > 0:
        user = User.query.filter_by(username=username).first()
        if not n_clicks:
            print(f'no {n_clicks}')
            raise PreventUpdate
        print(user)
        if pathname == '/success_login':
            raise PreventUpdate
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                print(f'loged {pathname}')
                return ['/success_login', pathname]
    raise PreventUpdate



################################################################################
# LOGIN BUTTON CLICKED / ENTER PRESSED - RETURN RED BOXES IF LOGIN DETAILS INCORRECT
################################################################################
@app.callback(Output('usernameBox', 'className'),
              [Input('loginButton', 'n_clicks'),
               Input('usernameBox', 'n_submit'),
               Input('passwordBox', 'n_submit')],
              [State('usernameBox', 'value'),
               State('passwordBox', 'value')])
def update_output(n_clicks, usernameSubmit, passwordSubmit, username, password):
    if (n_clicks > 0) or (usernameSubmit > 0) or (passwordSubmit) > 0:
        user = User.query.filter_by(username=username).first()
        if user:
            return 'form-control'
        else:
            return 'form-control is-invalid'
    else:
        return 'form-control'


################################################################################
# LOGIN BUTTON CLICKED / ENTER PRESSED - RETURN RED BOXES IF LOGIN DETAILS INCORRECT
################################################################################
@app.callback(Output('passwordBox', 'className'),
              [Input('loginButton', 'n_clicks'),
               Input('usernameBox', 'n_submit'),
               Input('passwordBox', 'n_submit')],
              [State('usernameBox', 'value'),
               State('passwordBox', 'value')])
def update_output(n_clicks, usernameSubmit, passwordSubmit, username, password):
    if (n_clicks > 0) or (usernameSubmit > 0) or (passwordSubmit) > 0:
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                return 'form-control'
            else:
                return 'form-control is-invalid'
        else:
            return 'form-control is-invalid'
    else:
        return 'form-control'
