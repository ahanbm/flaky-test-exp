
import numpy as np
import unittest
import tensorflow as tf
import torch
import random

class Tests(unittest.TestCase):

    def test_instrumentation(self):
        x = 0.5
        y = 0.6
        print('log>>>', x)
        print('log>>>', y)
        assert (x <= y)
        random_numbers = np.random.rand(5)
        print('log>>>', np.sum(random_numbers))
        print('log>>>', 1.0)
        self.assertGreater(np.sum(random_numbers), 1.0, 'Sum of random numbers should be greater than 1.0')
        random_tensor_torch = torch.rand(5)
        print('log>>>', torch.sum(random_tensor_torch).item())
        print('log>>>', 2.5)
        np.testing.assert_allclose(torch.sum(random_tensor_torch).item(), 2.5, atol=2, err_msg='Sum of tensor should be close to 1.5')
        tensor_a = tf.random.uniform(shape=(3,), minval=0, maxval=5)
        tensor_b = tf.random.uniform(shape=(3,), minval=0, maxval=5)
        print('log>>>', tensor_a)
        print('log>>>', tensor_b)
        tf.test.TestCase().assertAllClose(tensor_a, tensor_b, rtol=2, atol=2, msg='Tensors are not close enough')
        random_tensor_np = np.random.rand(3, 3)
        print('log>>>', random_tensor_np)
        print('log>>>', 1.1)
        np.testing.assert_array_less(random_tensor_np, 1.1, 'Expected all elements in the tensor to be < 1.1')
        random_value = random.random()
        print('log>>>', random_value)
        print('log>>>', 0)
        self.assertGreaterEqual(random_value, 0, 'Expected random_value to be >= 0')
        print('log>>>', random_value)
        print('log>>>', 1)
        self.assertLessEqual(random_value, 1, 'Expected random_value to be <= 1')
        print('log>>>', x)
        print('log>>>', y)
        self.assertAlmostEqual(x, y, delta=0.2, msg='Expected x and y to be approximately equal within a delta of 0.2')
if (__name__ == '__main__'):
    unittest.main()
