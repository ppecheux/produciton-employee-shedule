"In this file, we want to assign stations to activity blocks"
import pandas as pd
import numpy as np


def assign_stations(activities: list, products: list, nb_stations: int) -> dict:
    # df = pd.read_json(activities, encoding='records')
    df = pd.DataFrame.from_records(activities)
    if df.empty:
        return []

    df = fill_sequence_rank(df)

    df_weighted_avg = activities_weighted_avg(
        df, pd.DataFrame.from_records(products))

    df_weighted_avg = assign_stations_for_avg(df_weighted_avg, nb_stations)
    df = df[df.columns.difference(['min_sequence_rank', 'max_sequence_rank'])]
    df = df.join(df_weighted_avg, on='activity_block_name')

    df = df[['product', 'activity_block_name',
             'activity_block_duration', 'station_nb']]

    activities = df.to_dict('rows')
    return activities

def fill_sequence_rank(df: pd.DataFrame) -> pd.DataFrame:
    if df['min_sequence_rank'].isnull().all() or df['max_sequence_rank'].isnull().all():
        if df['min_sequence_rank'].isnull().all():
            if df['max_sequence_rank'].isnull().all():
                df['max_sequence_rank'] = 0
            df['min_sequence_rank'] = df['max_sequence_rank'].dropna().min()    
        else:
            df['max_sequence_rank'] = df['min_sequence_rank'].dropna().max()

    df.loc[pd.isna(df.min_sequence_rank), 'min_sequence_rank'] = df['min_sequence_rank'].dropna().min()
    df.loc[pd.isna(df.max_sequence_rank), 'max_sequence_rank'] = df['max_sequence_rank'].dropna().max()
    return df

def assign_stations_for_avg(df_weighted_avg: pd.DataFrame, nb_stations: int) -> pd.DataFrame:
    df_weighted_avg['station_nb'] = [np.nan] * len(df_weighted_avg)

    min_sequence_rank = set(df_weighted_avg['min_sequence_rank'].unique())
    max_sequence_rank = set(df_weighted_avg['max_sequence_rank'].unique())
    unique_ranks = sorted(list(min_sequence_rank | max_sequence_rank))

    # compute time per station:
    rest_production_duration = df_weighted_avg['weighted_average'].sum()
    rest_nb_stations = nb_stations
    time_per_station = rest_production_duration/rest_nb_stations

    cummulated_duration = 0
    if isinstance(df_weighted_avg["weighted_average"].values[0], np.timedelta64):
        cummulated_duration = pd.Timedelta('0 days')

    station_nb = 1

    for rank in unique_ranks:
        possible_activities = df_weighted_avg[(df_weighted_avg.min_sequence_rank <= rank)
                                              & (df_weighted_avg.max_sequence_rank >= rank)
                                              & (pd.isna(df_weighted_avg.station_nb))]

        while len(possible_activities):
            possible_activities.loc[:,'dist_to_target_time'] = (time_per_station
                                                          - cummulated_duration
                                                          - possible_activities.weighted_average/2)

            activity = possible_activities.dist_to_target_time.idxmin()
            cummulated_duration_on_middle_of_activity = (cummulated_duration
                                                         + df_weighted_avg.loc[activity, 'weighted_average']/2)
            cummulated_duration += df_weighted_avg.loc[activity,
                                                       'weighted_average']
            while cummulated_duration_on_middle_of_activity > time_per_station:
                cummulated_duration_on_middle_of_activity = df_weighted_avg.loc[
                    activity, 'weighted_average']/2
                cummulated_duration = df_weighted_avg.loc[activity,
                                                          'weighted_average']
                station_nb += 1
                rest_nb_stations -= 1
                time_per_station = rest_production_duration/rest_nb_stations
            df_weighted_avg.loc[activity, "station_nb"] = station_nb
            possible_activities = possible_activities[possible_activities.index != activity]
            rest_production_duration -= df_weighted_avg.loc[activity,
                                                            'weighted_average']

    return df_weighted_avg


def activities_weighted_avg(df_activities, df_products) -> pd.DataFrame:
    df_products = df_products.groupby(['product']).sum()
    total_quantity_product = df_products.quantity.sum()
    df_activities = df_activities.join(df_products['quantity'], on='product')

    df_activities['duration_times_quantity'] = df_activities[
        'activity_block_duration'] * df_activities['quantity']
    if 'min_sequence_rank' in df_activities.columns:
        df_activities = (df_activities[['activity_block_name', 'duration_times_quantity', 'min_sequence_rank', 'max_sequence_rank']]
                     .groupby(['activity_block_name'])
                     .agg({'min_sequence_rank': 'max', 'max_sequence_rank': 'min', 'duration_times_quantity': 'sum'}))
    else:
        df_activities = (df_activities[['activity_block_name', 'duration_times_quantity']]
                     .groupby(['activity_block_name'])
                     .agg({'duration_times_quantity': 'sum'}))        
    df_activities['weighted_average'] = df_activities[
        'duration_times_quantity'] / total_quantity_product

    return df_activities