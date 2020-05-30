from sqlalchemy import Table
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from config import engine
from datetime import timedelta

db = SQLAlchemy()

class Activity(db.Model):
    product = db.Column(db.String(80), primary_key=True)
    activity_block_name = db.Column(db.String(80), primary_key=True)
    activity_block_duration = db.Column(db.Interval())
    station_nb =db.Column(db.Integer())

activityTable = Table('activity', Activity.metadata)

def create_activity_table():
    Activity.metadata.create_all(engine)

def add_Activity(product, activity_block_name, activity_block_duration, station_nb=None):
    if isinstance(activity_block_duration, (float, int)):
        activity_block_duration = timedelta(minutes=activity_block_duration)
    insert_stmt = activityTable.insert().values(
        product=product,
        activity_block_name=activity_block_name,
        activity_block_duration=activity_block_duration,
        station_nb=station_nb
    )
    conn = engine.connect()
    conn.execute(insert_stmt)
    conn.close()

def delete_Activity(product, activity_block_name):
    Activity.query.filter_by(
        product=product,
        activity_block_name=activity_block_name
    ).delete()
    db.session.commit()

def delete_all_activies():
    Activity.query.delete()
    db.session.commit()

def update_station_nb_Activity(product, activity_block_name, station_nb):
    Activity.query.filter_by(
        product=product,
        activity_block_name=activity_block_name
    ).update({Activity.station_nb: station_nb})
    db.session.commit()

def show_activities():
    select_stmt = select([Activity.c.product,
                        Activity.c.activity_block_name,
                        Activity.c.activity_block_duration,
                        Activity.c.station_nb])

    conn = engine.connect()
    results = conn.execute(select_stmt)

    activities = []

    for result in results:
        activities.append({
            'product' : result[0],
            'activity_block_name' : result[1],
            'activity_block_duration' : result[2],
            'station_nb' : result[3]
        })

    conn.close()
    print(activities)
    return activities