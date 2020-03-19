import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import pandas as pd
import numpy as np
from algos.stations import assign_stations

class TestAssignStations(unittest.TestCase):

    def test_all_activities_are_assigned(self):
        df = pd.DataFrame({
            "cabine": ["cabineA", "cabineA", "cabineB", "cabineB"],
            "activity": ["activity1", "activity2", "activity1", "activity2"],
            "duration":  [pd.Timedelta(minutes=1), pd.Timedelta(minutes=1), pd.Timedelta(minutes=1), pd.Timedelta(minutes=1)],
            "station": [np.nan]*4
        })
        print(df)
        records = df.to_json(orient='records')
        print(records)
        records_with_stations = assign_stations(activities=records, nb_stations=1)
        df_with_stations = pd.read_json(records_with_stations, orient='records')

        self.assertFalse(df_with_stations.station.isnull().values.any())

    def weighted_average(self):

        #Creating a dataframe for the test

        df = pd.DataFrame({
            "cabineA":[12, 15, 25,24],
            "cabineB":[26,27,19,12],
            "cabineC":[14,28,22,16]},
            index = ["act1","act2", "act3", "act4"])

        Nb_cabs = [20, 14, 8]  #Number of cabs in a list

        tab = df.to_numpy()    #Dataframe to numpy to be able to calculate the weighted average

        nb_act =tab.shape[0]   #Number of activities

        Weig_avg = []          #Creating an empty list where we will put the weighted avg for each activity

        avg = 0                #temp variables
        Nb_cabs_tot = 0


        for i in range (len(Nb_cabs)-1):
            Nb_cabs_tot += Nb_cabs[i]       #Number total of cabs

        for i in range (nb_act-1):          #Determination of the weighted avg of each activity
            for j in range (2):
                avg += tab[i][j] * Nb_cabs[j]
            avg = avg/Nb_cabs_tot
            Weig_avg.append(avg)


        print(Weig_avg)

    def test_limited_nb_of_stations_used(self):
        nb_stations = 2
        df = pd.DataFrame({
            "cabine": ["cabineA", "cabineA", "cabineB", "cabineB"],
            "activity": ["activity1", "activity2", "activity1", "activity2"],
            "duration":  [pd.Timedelta(minutes=1), pd.Timedelta(minutes=1), pd.Timedelta(minutes=1), pd.Timedelta(minutes=1)],
            "station": ['sation1', 'station3', 'station2', 'station3']
        })
        records = df.to_json(orient='records')
        records_with_stations = assign_stations(activities=records, nb_stations=nb_stations)
        df_with_stations = pd.read_json(records_with_stations, orient='records')

        self.assertTrue(len(df_with_stations.station.unique())<=nb_stations)

    def test_stations_are_not_overlapping(self):
        df = pd.DataFrame({
            "cabine": ["cabineA", "cabineA", "cabineB", "cabineB"],
            "activity": ["activity1", "activity2", "activity1", "activity2"],
            "duration":  [pd.Timedelta(minutes=1), pd.Timedelta(minutes=1), pd.Timedelta(minutes=1), pd.Timedelta(minutes=1)],
            "station": ['sation1', 'station3', 'station2', 'station3']
        })

        records = df.to_json(orient='records')
        records_with_stations = assign_stations(activities=records, nb_stations=1)
        df = pd.read_json(records_with_stations, orient='records')

        for station in df.station.unique():
            df_station = df[df.station == station]
            self.assertEqual(df_station.station.count(), 1 + df_station.index.max() - df_station.index.min())




if __name__ == "__main__":
    unittest.main()