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
            "quantity": [8, 8]
        })

    def test_all_employees_are_assigned(self):

        records = self.df_activities.to_records()
        records_with_employees = assign_employee(activities=records,
                                                table_nb_products=self.df_product.to_records(),
                                                input_shift_duration_hour=8,
                                                input_operator_efficiency=1)
        df_with_employees = pd.DataFrame.from_dict(records_with_employees)
        self.assertFalse(df_with_employees.operator_nb.isnull().values.any())

    def test_is_assigned_for_one_task(self):
        records = pd.DataFrame({
            "product": ["cabineA"],
            "activity_block_name": ["activity1"],
            "activity_block_duration":  [1],
            "station_nb": [1],         
        }).to_records()

        products = pd.DataFrame({"product" : ["cabineA"], "quantity": [8]}).to_records()

        records_with_employees = assign_employee(activities=records,
                                                table_nb_products= products,
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
            'employee_nb': [1,1,2,2]
        }).set_index('activity_block_name')
        result = assign_employee_every_two_stations(df_stations_activities)
        self.assertTrue(result.equals(expected))

    def test_assign_employees_like_stations(self):
        df_stations_activities = pd.DataFrame({
            "activity_block_name": ["activity1", "activity2", "activity3", "activity4"],
            'daily_duration': [6]*4,
            "station_nb": [i for i in range(4)],
        }).set_index('activity_block_name')

        expected = pd.DataFrame({
            "activity_block_name": ["activity1", "activity2", "activity3", "activity4"],
            'daily_duration': [6]*4,
            "station_nb": [i for i in range(4)],
            'operator_nb': [1,2,3,4]
        }).set_index('activity_block_name')


        result = assign_employees_like_stations(df_stations_activities, 4, 7, 1)
        self.assertTrue(result.equals(expected))

    def test_assign_employees_like_stations_no_more_two_stations(self):
        df_stations_activities = pd.DataFrame({
            "activity_block_name": ["activity1", "activity2", "activity3", "activity4"],
            'daily_duration': [1,1,1,6],
            "station_nb": [i for i in range(4)],
        }).set_index('activity_block_name')

        expected = pd.DataFrame({
            "activity_block_name": ["activity1", "activity2", "activity3", "activity4"],
            'daily_duration': [1,1,1,6],
            "station_nb": [i for i in range(4)],
            'operator_nb': [1,1,2,2]
        }).set_index('activity_block_name')

        result = assign_employees_like_stations(df_stations_activities, 2, 7, 1)

        self.assertTrue(result.equals(expected))

    def test_assign_employees_with_time_delta(self):
        df_stations_activities = pd.DataFrame({
            "activity_block_name": ["activity1", "activity2", "activity3", "activity4"],
            'daily_duration': [pd.Timedelta(hours=1),pd.Timedelta(hours=1),pd.Timedelta(hours=1),pd.Timedelta(hours=6)],
            "station_nb": [i for i in range(4)],
        }).set_index('activity_block_name')

        expected = pd.DataFrame({
            "activity_block_name": ["activity1", "activity2", "activity3", "activity4"],
            'daily_duration': [pd.Timedelta(hours=1),pd.Timedelta(hours=1),pd.Timedelta(hours=1),pd.Timedelta(hours=6)],
            "station_nb": [i for i in range(4)],
            'operator_nb': [1,1,2,2]
        }).set_index('activity_block_name')

        result = assign_employees_like_stations(df_stations_activities, 2, 7, 1)

        self.assertTrue(result.equals(expected))

    def test_employees_are_in_order_of_the_stations(self):
        nb_activities = 10
        df_stations_activities = pd.DataFrame({
            "activity_block_name": [f"activity{i}" for i in range(nb_activities)],
            'daily_duration': [pd.Timedelta(hours=1)]*nb_activities,
            "station_nb": list(range(nb_activities)),
        }).set_index('activity_block_name')

        result = assign_employees_like_stations(df_stations_activities, nb_activities, 7, 1)

        result.sort_values(by='station_nb', inplace=True)
        self.assertTrue(result['operator_nb'].is_monotonic_increasing)        

if __name__ == "__main__":
    unittest.main()