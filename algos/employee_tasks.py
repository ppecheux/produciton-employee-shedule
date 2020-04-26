"In this file, we want to assign people to activity blocks"
import pandas as pd
from algos.stations import activities_weighted_avg


def assign_employee(activities: list, table_nb_products: list, input_shift_duration_hour: int) -> dict:
    # use station weight avg to compute to workloads of each stations
    df = pd.DataFrame.from_records(activities)
    if df.empty:
        return []

    # begin algo
    df_weighted_avg = activities_weighted_avg(
        df, pd.DataFrame.from_records(table_nb_products))
    return activities