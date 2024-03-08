import numpy as np
import unittest

class Tests(unittest.TestCase):

    def test_func(self):
        x = 0.5
        y = 0.6
        assert (x < y)
        random_numbers = np.random.rand(5)
        self.assertTrue((np.sum(random_numbers) > 1.0))

if (__name__ == '__main__'):
    unittest.main()
