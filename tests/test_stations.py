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
        records = df.to_json(orient='records')
        records_with_stations = assign_stations(activities=records, nb_stations=1)
        df_with_stations = pd.read_json(records_with_stations, orient='records')

        self.assertFalse(df_with_stations.station.isnull().values.any())

if __name__ == "__main__":
    unittest.main()