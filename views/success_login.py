import dash_core_components as dcc
import dash_bootstrap_components as dbc


layout = dbc.Container([
    dcc.Store('url_login', storage_type='session', data=''),
    #dcc.Location('url2'),
])

# begin block to refresh after login


# @app.callback(Output('url', 'pathname'),
#               [
#  #   Input('url_login', 'data'),
#     Input('success_login_link', 'href')
# ])
# def trigger_success_view(
# #        url_login,
#         url_login2
# ):
#     if not url_login2 == '/success_login':
#         return url_login2
#     return '/success_login'

# @app.callback(Output('success_login_link', 'href'),
#               [Input('url2', 'pathname')],
#               [State('url_login', 'data')])
# def trigger_success_view(trigger, url_login):
#     if trigger == '/success_login':
#         return url_login
#     raise PreventUpdate

# end block to refresh after login
