import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import pandas as pd
import numpy as np
from algos.employee_tasks import assign_employee

class TestAssignStations(unittest.TestCase):

    def test_all_employees_are_assigned(self):
        df = pd.DataFrame({
            "cabine": ["cabineA", "cabineA", "cabineB", "cabineB"],
            "activity": ["activity1", "activity2", "activity1", "activity2"],
            "duration":  [pd.Timedelta(minutes=1), pd.Timedelta(minutes=1), pd.Timedelta(minutes=1), pd.Timedelta(minutes=1)],
            "station": ['station1']*4,
            "employee": [np.nan]*4
        })
        records = df.to_json(orient='records')
        records_with_employees = assign_employee(activities=records, nb_employees=1)
        df_with_employees = pd.read_json(records_with_employees, orient='records')

        self.assertFalse(df_with_employees.employee.isnull().values.any())


    def test_limited_nb_of_employees_used(self):
        nb_employees = 2
        df = pd.DataFrame({
            "cabine": ["cabineA", "cabineA", "cabineB", "cabineB"],
            "activity": ["activity1", "activity2", "activity1", "activity2"],
            "duration":  [pd.Timedelta(minutes=1), pd.Timedelta(minutes=1), pd.Timedelta(minutes=1), pd.Timedelta(minutes=1)],
            "station": ['station1']*4,
            "employee": ['op1', 'op3', 'op2', 'op3']
        })
        records = df.to_json(orient='records')
        records_with_employees = assign_employee(activities=records, nb_employees=nb_employees)
        df_with_employees = pd.read_json(records_with_employees, orient='records')

        self.assertTrue(len(df_with_employees.employee.unique())<=nb_employees)

if __name__ == "__main__":
    unittest.main()