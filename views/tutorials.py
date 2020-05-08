import datetime
import numpy as np
import pandas as pd
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

from algos.stations import assign_stations
from algos.stations import activities_weighted_avg

layout =html.Div(id='pageContent2',children=[
	 html.H1("Turorial Page")
	 ])