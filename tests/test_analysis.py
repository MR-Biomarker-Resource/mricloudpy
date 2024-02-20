import unittest
import pandas as pd
import plotly_express as px
from mricloudpy import data

class TestAnalysis(unittest.TestCase):

    def setUp(self):
        # Create data object and relevant testing items
        self.DATA_PATH = 'sample_data_covariate'
        self.COVARIATE_DATA_PATH = 'sample_data_covariate\hcp_sample_clean.csv'
        self.COVARIATE_DATAFRAME = pd.read_csv(self.COVARIATE_DATA_PATH)
        self.obj = data.Data(path=self.DATA_PATH, id_type='numeric')

        # Create covariate dataset
        self.covariate_data = self.obj.append_covariate_data(path=self.COVARIATE_DATA_PATH, icv=True, tbv=True)
    
    def test_OLS(self):
        # self.assertIsInstance(self.obj.OLS(self.covariate_data, 
        #                                    covariates=['Age', 
        #                                                'Cerebellum_L_Type1.0_L3.0', 
        #                                                'Hippo_L_Type1.0_L4.0'], 
        #                                     outcome='CSF_Type1.0_L1.0', 
        #                                     log=False), px.Fig)
        return
    
    def test_Logit(self):
        return

if __name__ == '__main__':
    unittest.main()