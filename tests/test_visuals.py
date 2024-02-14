import unittest
import pandas as pd
from mricloudpy import data

class TestVisuals(unittest.TestCase):

    def setUp(self):
        # Create data object and relevant testing items
        self.DATA_PATH = 'sample_data_covariate'
        self.COVARIATE_DATA_PATH = 'sample_data_covariate\hcp_sample_clean.csv'
        self.COVARIATE_DATAFRAME = pd.read_csv(self.COVARIATE_DATA_PATH)
        self.obj = data.Data(path=self.DATA_PATH, id_type='numeric')
    
    def test_generate_sunburst(self):
        return
    
    def test_generate_treemap(self):
        return
    
    def test_generate_icicle(self):
        return
    
    def test_generate_bar(self):
        return
    
    def test_generate_mean_diff(self):
        return
    
    def test_generate_corr_matrix(self):
        return

if __name__ == '__main__':
    unittest.main()