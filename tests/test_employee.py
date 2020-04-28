import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import pandas as pd
import numpy as np
from algos.employee_tasks import assign_employee, assign_employee_every_two_stations
from algos.employee_tasks import assign_employees_like_stations
class TestAssignStations(unittest.TestCase):

    def __init__(self, methodName):
        super().__init__(methodName)
        self.df_activities = pd.DataFrame({
            "product": ["cabineA", "cabineA", "cabineB", "cabineB"],
            "activity_block_name": ["activity1", "activity2", "activity1", "activity2"],
            "activity_block_duration":  [1]*4,
            "station_nb": ['station1']*4,
            "employee": [np.nan]*4
        })
        self.df_product = pd.DataFrame({
            "product": ["cabineA", "cabineB"],
            "quantity": [1, 1]
        })

    def test_all_employees_are_assigned(self):

        records = self.df_activities.to_records()
        records_with_employees = assign_employee(activities=records,
                                                table_nb_products=self.df_product.to_records(),
                                                input_shift_duration_hour=8,
                                                input_operator_efficiency=1)
        df_with_employees = pd.DataFrame.from_dict(records_with_employees)
        self.assertFalse(df_with_employees.operator_nb.isnull().values.any())

    def test_assign_employee_every_two_stations(self):
        df_stations_activities = pd.DataFrame({
            "activity_block_name": ["activity1", "activity2", "activity3", "activity4"],
            "station_nb": [i for i in range(4)],
        }).set_index('activity_block_name')

        expected = pd.DataFrame({
            "activity_block_name": ["activity1", "activity2", "activity3", "activity4"],
            "station_nb": list(range(4)),
            'employee_nb': [0,0,1,1]
        }).set_index('activity_block_name')
        result = assign_employee_every_two_stations(df_stations_activities)
        self.assertTrue(result.equals(expected))

    def test_assign_employees_like_stations(self):
        df_stations_activities = pd.DataFrame({
            "activity_block_name": ["activity1", "activity2", "activity3", "activity4"],
            'weighted_average': [6]*4,
            "station_nb": [i for i in range(4)],
        }).set_index('activity_block_name')

        expected = pd.DataFrame({
            "activity_block_name": ["activity1", "activity2", "activity3", "activity4"],
            'weighted_average': [6]*4,
            "station_nb": [i for i in range(4)],
            'operator_nb': [0,1,2,3]
        }).set_index('activity_block_name')


        result = assign_employees_like_stations(df_stations_activities, 4, 7, 1)
        self.assertTrue(result.equals(expected))

    def test_assign_employees_like_stations_no_more_two_stations(self):
        df_stations_activities = pd.DataFrame({
            "activity_block_name": ["activity1", "activity2", "activity3", "activity4"],
            'weighted_average': [1]*4,
            "station_nb": [i for i in range(4)],
        }).set_index('activity_block_name')

        expected = pd.DataFrame({
            "activity_block_name": ["activity1", "activity2", "activity3", "activity4"],
            'weighted_average': [1]*4,
            "station_nb": [i for i in range(4)],
            'operator_nb': [0,0,1,1]
        }).set_index('activity_block_name')

        result = assign_employees_like_stations(df_stations_activities, 2, 7, 1)
        print(result)

        self.assertTrue(result.equals(expected))

if __name__ == "__main__":
    unittest.main()