import unittest
from mricloudpy import data

class TestData(unittest.TestCase):

    def setUp(self):
        # Create data object and relevant testing items
        self.DATA_PATH = 'sample_data_covariate'
        self.obj = data.Data(path=self.DATA_PATH, id_type='numeric')
    
    def test_data(self):
        # Check Data object type and if parameters are valid
        self.assertIsInstance(self.obj, data.Data)
        self.assertEqual(self.obj.path, self.DATA_PATH)
        self.assertEqual(self.obj.id_type, 'numeric')
        self.assertEqual(self.obj.id_list, None)
        self.assertTrue(self.obj.df.equals(self.obj.get_data()))

if __name__ == '__main__':
    unittest.main()