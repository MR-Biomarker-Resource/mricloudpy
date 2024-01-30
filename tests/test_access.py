import unittest
import pandas as pd
import numpy as np
from mricloudpy import data

class TestAccess(unittest.TestCase):

    def setUp(self):
        # Create data object and relevant testing items
        self.DATA_PATH = 'sample_data_covariate'
        self.obj = data.Data(path=self.DATA_PATH, id_type='numeric')
    
    def test_rename_subject(self):
        # Check if new subject ID matches
        self.assertEqual('test', self.obj.rename_subject('0', 'test').iloc[0,0])

    def test_get_data(self):
        # Check if DataFrame data matches
        self.assertTrue(self.obj.df.equals(self.obj.get_data()))

    def test_get_id(self):
        # Check if IDs match
        np.testing.assert_array_equal(self.obj.get_id(), self.obj.df['ID'].unique())

    def test_long_to_wide(self):
        # Check if IDs match
        np.testing.assert_array_equal(self.obj.long_to_wide().index, self.obj.df['ID'].unique())

        # Check if columns are valid
        type_columns = [col for col in self.obj.long_to_wide().columns if '_Type' in col]
        self.assertTrue(len(type_columns) >= 10)

    # def test_normalize_covariate_data(self):
    #     self.assertEqual()

if __name__ == '__main__':
    unittest.main()