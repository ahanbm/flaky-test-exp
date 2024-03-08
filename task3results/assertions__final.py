
import numpy as np
import unittest

class Tests(unittest.TestCase):
    np.random.seed(42)

    def test_func(self):
        x = 0.5
        y = 0.6
        print('log>>>', y)
        print('log>>>', x)
        assert (x < y)

    def test_func2(self):
        random_numbers = np.random.rand(5)
        self.assertTrue((np.sum(random_numbers) > 1.0))
if (__name__ == '__main__'):
    unittest.main()
