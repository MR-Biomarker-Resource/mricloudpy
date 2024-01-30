import unittest
import pandas as pd
from mricloudpy import data

class TestRead(unittest.TestCase):

    def setUp(self):
        # Create data object and relevant testing items
        self.DATA_PATH = 'sample_data_covariate'
        self.COVARIATE_DATA_PATH = 'sample_data_covariate\hcp_sample_clean.csv'
        self.COVARIATE_DATAFRAME = pd.read_csv(self.COVARIATE_DATA_PATH)
        self.obj = data.Data(path=self.DATA_PATH, id_type='numeric')
    
    def test_append_covariate_data(self):
        # Create covariate dataset
        self.covariate_dataset = self.obj.append_covariate_data(path=self.COVARIATE_DATA_PATH, icv=True, tbv=True)

        # Check if first column is 'ID'
        self.assertEqual(self.covariate_dataset.columns[0], 'ID')

        # Check if covariate DataFrame columns are found in covariate dataset
        for col in self.COVARIATE_DATAFRAME.columns[1:]:
            self.assertIn(col, self.covariate_dataset.columns[1:])

if __name__ == '__main__':
    unittest.main()