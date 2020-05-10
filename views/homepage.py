import datetime
from dash import callback_context
from app import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_table
from views.functions_for_views.functions_for_callbacks import update_table_from_upload, data_table_nb_products
from views.functions_for_views.input_components import takt_time_input

layout = html.Div(id='backgroundimage',children=[
    html.Div(id='firstpage',children=["Bem vindo! Este é o Software de Line Balancinga DAF. Clique nas opções asima para ser redirecionado à página de interess"]),
    html.Hr(id="horizontalLine"),
    html.Div(id='firstpage',children=["Please make sure you launch all of the algorithm in the right order.\n"]),
    html.Hr(id="horizontalLine"),
    html.Div(id='firstpage', children=["If you have any doubts on how to use the app, please refer to the tutorial page"]),
    html.Hr(id="horizontalLine"),
    ])
  
