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
        if not possible:
            break
        df_operators = possible

    if (nb_stations+1)//2 - 1 == nb_operators:
        df_operators = assign_employee_every_two_stations(df_stations_activities)

    df = df.merge(df_operators, how='left',
                  left_index=True, suffixes=('', '_op'))

    return activities


def assign_employees_like_stations(df_stations_activities: pd.DataFrame, nb_operators: int, shift_duration:int, efficiency: float) -> pd.DataFrame:
    df_stations_activities['operator_nb'] = [np.nan] * len(df_stations_activities)
    

    cumulated_duration = 0
    rest_production_duration = df_stations_activities['weighted_average'].sum()
    duration_operator = shift_duration*efficiency
    total_working_duration = duration_operator*nb_operators
    if rest_production_duration > total_working_duration:
        return None

    operator_nb = 0

    for activity in df_stations_activities.index:
        cumulated_duration += df_stations_activities.loc[activity, 'weighted_average']
        if cumulated_duration > duration_operator:
            cumulated_duration = df_stations_activities.loc[activity, 'weighted_average']
            operator_nb += 1
            nb_operators -= 1
        print(type(rest_production_duration))
        print(f'my duration {rest_production_duration}')
        print(df_stations_activities)
        rest_production_duration -= df_stations_activities.loc[activity, 'weighted_average']
        df_stations_activities.loc[activity, 'operator_nb'] = operator_nb
    df_stations_activities['operator_nb'] = df_stations_activities['operator_nb'].astype(int)
    if 0 > nb_operators:
        return None
    else:
        return df_stations_activities


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
