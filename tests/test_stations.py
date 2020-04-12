import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algos.stations import weighted_average, activities_weighted_avg
from algos.stations import assign_stations
import numpy as np
import pandas as pd
import unittest


class TestAssignStations(unittest.TestCase):

    def __init__(self, methodName):
        super().__init__(methodName)
        self.df_activities = pd.DataFrame({
            "product": ["cabineA", "cabineA", "cabineB", "cabineB"],
            "activity_block_name": ["activity1", "activity2", "activity1", "activity2"],
            "activity_block_duration":  [pd.Timedelta(minutes=1), pd.Timedelta(minutes=1), pd.Timedelta(minutes=1), pd.Timedelta(minutes=1)],
            "fixed_station_nb": [np.nan]*4
        })
        self.df_product = pd.DataFrame({
            "product": ["cabineA", "cabineB"],
            "quantity": [1, 1]
        })

    def test_all_activities_are_assigned(self):
        records = self.df_activities.to_records()
        records_with_stations = assign_stations(
            activities=records, nb_stations=1, products=self.df_product)
        df_with_stations = pd.DataFrame.from_dict(records_with_stations)
        self.assertFalse(df_with_stations.station_nb.isnull().values.any())

    def test_weighted_average(self):

        # Creating a dataframe for the test
        df = pd.DataFrame({
            "cabine1": [12, 15, 25, 24, 16],
            "cabine2": [26, 27, 19, 12, 18],
            "cabine3": [14, 28, 22, 16, 23]},
            index=["act1", "act2", "act3", "act4", "act5"])

        # Make sure that the weighted average is right
        Nb_cabs1 = [20, 14, 8]
        df_test = weighted_average(df, Nb_cabs1)
        self.assertEqual(
            df_test.loc["act5", "Weighted average"], ((16*20+18*14+23*8)/(20+14+8)))
        # Make sure that the weighted average is right with zero cabs
        Nb_cabs2 = [0, 10, 8]
        df_test2 = weighted_average(df, Nb_cabs2)
        self.assertEqual(
            df_test2.loc["act3", "Weighted average"], ((19*10+22*8)/(10+8)))

    def test_limited_nb_of_stations_used(self):
        nb_stations = 2
        df = self.df_activities
        df['fixed_station_nb'] = ['sation1', 'station3', 'station2', 'station3']
        records = df.to_records()
        records_with_stations = assign_stations(
            activities=records, nb_stations=nb_stations, products=self.df_product)
        df_with_stations = pd.DataFrame.from_dict(records_with_stations)

        self.assertTrue(len(df_with_stations.station_nb.unique()) <= nb_stations)

    def futur_test_stations_are_not_overlapping(self):
        df = self.df_activities
        df['fixed_station_nb'] = ['sation1', 'station3', 'station2', 'station3']

        records = df.to_records()
        records_with_stations = assign_stations(
            activities=records, nb_stations=1, products=self.df_product)
        df = pd.DataFrame.from_dict(records_with_stations)

        print(df)

        for station in df.station_nb.unique():
            df_station = df[df.station_nb == station]
            self.assertEqual(df_station.station_nb.count(), 1 +
                             df_station.index.max() - df_station.index.min())

    def test_one_product_average_station(self):
        df =  pd.DataFrame({
                "product": ["cabineA"] * 2,
                "activity_block_name": ["activity1", "activity2"],
                "activity_block_duration":  [pd.Timedelta(minutes=1), pd.Timedelta(minutes=2)],
                "fixed_station_nb": [np.nan]*2
            })

        df_products = pd.DataFrame({
            "product": ["cabineA"],
            "quantity": [2]
        })

        df_w = activities_weighted_avg(df, df_products)
        self.assertEqual(list(df_w.weighted_average.values), list(df.activity_block_duration.values))

    def test_one_activity_average_station(self):
        df =  pd.DataFrame({
                "product": ["cabineA", "cabineB", "cabineC"],
                "activity_block_name": ["activity1"] * 3,
                "activity_block_duration":  [pd.Timedelta(minutes=1), pd.Timedelta(minutes=2), pd.Timedelta(minutes=3)],
                "fixed_station_nb": [np.nan]*3
            })

        df_products = pd.DataFrame({
            "product": ["cabineA", "cabineB", "cabineC"],
            "quantity": [1] * 3
        })

        df_w = activities_weighted_avg(df, df_products)
        self.assertEqual(pd.to_timedelta(df_w.weighted_average.values[0]), df.activity_block_duration.mean())

    def test_assign_station_one_product_two_stations(self):
        df_activities = pd.DataFrame({
            "product": ["cabineA", "cabineA"],
            "activity_block_name": ["activity1", "activity2"],
            "activity_block_duration":  [pd.Timedelta(minutes=1), pd.Timedelta(minutes=1)],
            "fixed_station_nb": [np.nan]*2
        })
        df_product = pd.DataFrame({
            "product": ["cabineA"],
            "quantity": [1]
        })
        stations = assign_stations(df_activities.to_records(), df_product.to_records(), 2)
        df_stations = pd.DataFrame.from_records(stations)
        self.assertEqual(list(df_stations.station_nb.values), [1, 2])

if __name__ == "__main__":
    unittest.main()
