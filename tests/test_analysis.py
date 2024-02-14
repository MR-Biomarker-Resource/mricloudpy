import unittest
import pandas as pd
from mricloudpy import data

class TestAnalysis(unittest.TestCase):

    def setUp(self):
        # Create data object and relevant testing items
        self.DATA_PATH = 'sample_data_covariate'
        self.COVARIATE_DATA_PATH = 'sample_data_covariate\hcp_sample_clean.csv'
        self.COVARIATE_DATAFRAME = pd.read_csv(self.COVARIATE_DATA_PATH)
        self.obj = data.Data(path=self.DATA_PATH, id_type='numeric')
    
    def test_OLS(self):
        return
    
    def test_Logit(self):
        return

if __name__ == '__main__':
    unittest.main()