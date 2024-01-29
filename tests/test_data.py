import unittest
import mricloudpy

class TestData(unittest.TestCase):
    
    def test_Data(self):
        DATA_PATH = 'sample_data_covariate'
        obj = mricloudpy.Data(path=DATA_PATH, id_type='numeric')  # replace with your actual function
        self.assertIsInstance(obj, mricloudpy.data.Data)  # replace with your actual class

if __name__ == '__main__':
    unittest.main()