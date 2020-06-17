"In this file, we want to assign people to activity blocks"
import pandas as pd
import numpy as np
from algos.stations import activities_weighted_avg


def assign_employee(activities: list, table_nb_products: list, input_shift_duration_hour: int, input_operator_efficiency: float) -> dict:
    df = pd.DataFrame.from_records(activities)
    if df.empty:
        return []

    df_products = pd.DataFrame.from_records(table_nb_products)
    df_weighted_avg = activities_weighted_avg(
        df, df_products)

    df_stations_activities = df[['station_nb', 'activity_block_name']].groupby(
        ['activity_block_name']).last()
    df_stations_activities = df_weighted_avg.join(df_stations_activities)
    df_stations_activities['daily_duration'] = df_stations_activities['weighted_average'] * df_products['quantity'].sum()

    nb_stations = df_stations_activities['station_nb'].nunique()
    print(nb_stations)
    nb_operators = (nb_stations+1)//2
    solution = None
    while solution is None:
        print(nb_operators)
        solution = assign_employees_like_stations(df_stations_activities,
                                                  nb_operators, input_shift_duration_hour, input_operator_efficiency)
        nb_operators += 1
    df_operators = solution
    df = df[["product", "activity_block_name", "activity_block_duration", "station_nb"]].merge(df_operators['operator_nb'], how='left',
                                                                                               right_index=True, left_on='activity_block_name')

    return df.to_dict('rows')


def assign_employees_like_stations(df_stations_activities: pd.DataFrame, nb_operators: int, shift_duration: int, efficiency: float) -> pd.DataFrame:
    df_stations_activities['operator_nb'] = [
        np.nan] * len(df_stations_activities)

    cumulated_duration = 0
    rest_production_duration = df_stations_activities['daily_duration'].sum()
    if isinstance(df_stations_activities["daily_duration"].iloc[0], pd.Timedelta):      
        cumulated_duration = pd.Timedelta('0 days')
        if not isinstance(shift_duration, np.timedelta64):
            shift_duration = pd.Timedelta(hours=shift_duration)
    else:
        shift_duration = shift_duration*60
    

    duration_operator = shift_duration*efficiency/100
    total_working_duration = duration_operator*nb_operators
    
    if rest_production_duration > total_working_duration:
        return None

    rest_nb_operators = nb_operators
    duration_operator = min(
        duration_operator, rest_production_duration/rest_nb_operators)

    operator_nb = 1
    working_on_stations = set()
    df_stations_activities.sort_values(by='station_nb', inplace=True)
    working_on_stations.add(df_stations_activities['station_nb'].iloc[0])
    for activity in df_stations_activities.index:
        cummulated_duration_on_middle_of_activity = cumulated_duration + df_stations_activities.loc[activity,'daily_duration']/2
        cumulated_duration += df_stations_activities.loc[activity,'daily_duration']
        current_station = df_stations_activities.loc[activity, 'station_nb']
        if cummulated_duration_on_middle_of_activity > duration_operator or cumulated_duration > shift_duration or len(working_on_stations) > 2:
            cummulated_duration_on_middle_of_activity = df_stations_activities.loc[activity, 'daily_duration']/2
            
            cumulated_duration = df_stations_activities.loc[activity,'daily_duration']
            operator_nb += 1
            started_on_station = df_stations_activities['station_nb']
            rest_nb_operators -= 1
            if rest_nb_operators*shift_duration < rest_production_duration:
                return None 
            duration_operator = rest_production_duration/rest_nb_operators
            working_on_stations = set()
            working_on_stations.add(current_station)

        rest_production_duration -= df_stations_activities.loc[activity, 'daily_duration']
        df_stations_activities.loc[activity, 'operator_nb'] = operator_nb
        working_on_stations.add(current_station)

    df_stations_activities['operator_nb'] = df_stations_activities['operator_nb'].astype(
        int)
    if 0 >= rest_nb_operators:
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
    df_stations_activities['employee_nb'] = df_stations_activities['employee_nb'] + 1
    return df_stations_activities
