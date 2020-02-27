# Dash app initialization
import dash
# User management initialization
import os
from flask_login import LoginManager, UserMixin
from users_mgt import db, User as base
from config import config


app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True


# config
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI=config.get('database', 'con'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db.init_app(server)

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

# Create User class with UserMixin


class User(UserMixin, base):
    pass

# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


COLORS = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'   # blue-teal
]

LEUZE_COLORS = {'navigation': '#605E5C',
                'tabelle': ['#627080', '#95A3B3'],
                'rahmen': '#EFEFEF',
                'KPI-Perf': '#404A54',
                'KPI-Effec': '#008800',
                'KPI-Avail': '#118DFF',
                'KPI-Quali': '#12239E',
                'Target-Farbe bei den KPIs': '#AF1037'}

SECOND_TO_DATE = {
    #1: 'second',
    60: 'minute',
    3600: 'hour',
    86400: 'day',
    604800: 'week',
    86400*30: 'month',
    31536000: 'year'
}
