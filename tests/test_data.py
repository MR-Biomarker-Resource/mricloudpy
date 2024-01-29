import unittest
import mricloudpy
import pandas as pd

class TestData(unittest.TestCase):

    def setUp(self):
        self.DATA_PATH = 'sample_data_covariate'
        self.obj = mricloudpy.Data(path=self.DATA_PATH, id_type='numeric')
    
    def test_data(self):
        self.assertIsInstance(self.obj, mricloudpy.data.Data)
        self.assertEqual(self.obj.path, self.DATA_PATH)
        self.assertEqual(self.obj.id_type, 'numeric')
        self.assertEqual(self.obj.id_list, None)
        self.assertTrue(self.obj.df.equals(self.obj.get_data()))

if __name__ == '__main__':
    unittest.main()