"In this file, we want to assign people to activity blocks"
import pandas as pd
import numpy as np
from algos.stations import activities_weighted_avg


def assign_employee(activities: list, table_nb_products: list, input_shift_duration_hour: int, input_operator_efficiency: float) -> dict:
    df = pd.DataFrame.from_records(activities)
    if df.empty:
        return []

    print(df)
    df_products = pd.DataFrame.from_records(table_nb_products)
    print(df_products)
    df_weighted_avg = activities_weighted_avg(
        df, df_products)

    df_stations_activities = df[['station_nb', 'activity_block_name']].groupby(
        ['activity_block_name']).last()
    df_stations_activities = df_weighted_avg.join(
        df_stations_activities)
    print(df_stations_activities)

    nb_stations = df_stations_activities['station_nb'].nunique()
    nb_operators = (nb_stations+1)//2
    while nb_operators > 1:
        nb_operators -= 1
        possible = assign_employees_like_stations()
        if possible.empty:
            break
        df_operators = possible

    if (nb_stations+1)//2 - 1 == nb_operators:
        df_operators = assign_employee_every_two_stations()

    df = df.merge(df_operators, how='left',
                  left_index=True, suffixes=('', '_op'))

    return activities


def assign_employees_like_stations():
    return pd.DataFrame()


def assign_employee_every_two_stations(df_stations_activities: pd.DataFrame) -> pd.DataFrame:
    activity_numbers = np.array(df_stations_activities['station_nb'].unique())
    df_employee_station = pd.DataFrame({
        'employee_nb': activity_numbers//2,
        'station_nb': list(df_stations_activities['station_nb'].unique())
    }).set_index('station_nb')
    df_stations_activities = df_stations_activities.merge(df_employee_station,
                                                          how='left',
                                                          right_index=True,
                                                          left_on="station_nb")

    return df_stations_activities
